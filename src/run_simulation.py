"""AI2-THOR — Yavaş Adımlı Yürüme ve Nesne Tutma (PDDL Uyumlu) Simülasyonu.

Bu betik:
1. Çift pencere (küçük Unity penceresi + tam ekran OpenCV penceresi) sorununu çözer.
   - Varsayılan olarak (USE_OPENCV = False) sadece AI2-THOR'un kendi Unity penceresi
     1024x768 boyutunda temiz tek bir uygulama olarak açılır.
   - İstenirse (USE_OPENCV = True) OpenCV HUD bilgi paneli ile pencereli modda çalıştırılabilir.
2. Hızlıca geçip aniden kapanma sorununu çözer.
   - Her adım arasında `STEP_DELAY` süresi kadar beklenir (yavaş, izlenebilir hareket).
   - İşlem bittiğinde aniden kapanmaz; kullanıcı terminalde Enter'a basana kadar sahne açık kalır.
3. wiki/pddl_mappings kurallarına uygun olarak:
   - Yavaş yürüme (MoveAhead, Rotate, LookDown)
   - Nesneye yaklaşma (GetInteractablePoses)
   - Nesneyi tutma (PickupObject: hand-empty, pickupable, visible, interactable)
   - Nesneyi taşıma ve tezgaha geri bırakma (PutObject)
   işlemlerini sırayla ve anlaşılır açıklamalarla yürütür.
"""

import time
from typing import Any, Dict, List, Optional, Tuple

import cv2
from ai2thor.controller import Controller

from src.thor_env import DEFAULT_HEIGHT, DEFAULT_WIDTH, SCENE, WINDOW_NAME, create_controller, verify_agent_position

# ==============================================================================
# AYARLAR (SETTINGS)
# ==============================================================================

# True yapılırsa hem Unity hem OpenCV penceresi (HUD bilgileriyle) açılır.
# False bırakılırsa SADECE tek bir pencere (AI2-THOR Unity) açılır ve çift uygulama karışıklığı olmaz.
USE_OPENCV: bool = False

# Her aksiyon arasındaki bekleme süresi (saniye cinsinden).
# Hareketlerin yavaş ve gözle takip edilebilir olmasını sağlar.
STEP_DELAY: float = 1.2

# Pencere çözünürlüğü (macOS ekranına tam oturan ideal boyut)
SCREEN_WIDTH: int = DEFAULT_WIDTH
SCREEN_HEIGHT: int = DEFAULT_HEIGHT

# Tercih edilen tutulabilir nesne tipleri (öncelik sırasıyla)
PREFERRED_PICKUP_TYPES: Tuple[str, ...] = ("Apple", "Mug", "Tomato", "Potato", "Bread", "Egg", "Plate")


# ==============================================================================
# YARDIMCI VE PDDL FONKSİYONLARI
# ==============================================================================

def log_header(title: str) -> None:
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)


def log_action_status(
    step_no: int,
    action: str,
    success: bool,
    pddl_rule: str = "",
    details: str = "",
) -> None:
    status_icon = "✓" if success else "✗"
    status_text = "BAŞARILI" if success else "BAŞARISIZ"
    print(f"[{step_no}] {status_icon} Aksiyon: {action:<18} Sonuç: {status_text}")
    if pddl_rule:
        print(f"    PDDL Ön Koşul / Kural : {pddl_rule}")
    if details:
        print(f"    Detay                : {details}")


def get_agent_info(controller: Controller) -> Dict[str, Any]:
    agent = controller.last_event.metadata.get("agent", {})
    pos = agent.get("position", {"x": 0.0, "y": 0.0, "z": 0.0})
    rot = agent.get("rotation", {"y": 0.0})
    horizon = agent.get("cameraHorizon", 0.0)
    is_standing = agent.get("isStanding", True)
    held_ids = controller.last_event.metadata.get("heldObjectIds", [])
    return {
        "pos": pos,
        "rot": rot.get("y", 0.0),
        "horizon": horizon,
        "standing": is_standing,
        "held_ids": held_ids,
        "hand_empty": len(held_ids) == 0,
    }


def draw_hud(frame: Any, action_name: str, step_no: int, agent_info: Dict[str, Any]) -> Any:
    """OpenCV penceresi için görsel bilgi katmanı (HUD) çizer."""
    img = frame.copy()
    h, w = img.shape[:2]

    # Yarı saydam üst panel
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (w, 85), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.75, img, 0.25, 0, img)

    # Yazılar
    title = f"AI2-THOR Simülasyonu ({SCENE}) — Adım {step_no}: {action_name}"
    cv2.putText(img, title, (15, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)

    pos = agent_info["pos"]
    pos_str = f"Pozisyon: x={pos['x']:.2f}, y={pos['y']:.2f}, z={pos['z']:.2f} | Yon: {agent_info['rot']:.0f} deg"
    cv2.putText(img, pos_str, (15, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1)

    hand_str = "El: BOS" if agent_info["hand_empty"] else f"El: TUTULUYOR ({agent_info['held_ids'][0]})"
    cv2.putText(img, hand_str, (15, 74), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100) if agent_info["hand_empty"] else (0, 165, 255), 1)

    return img


def update_display(
    controller: Controller,
    action_name: str,
    step_no: int,
    agent_info: Dict[str, Any],
) -> None:
    if not USE_OPENCV:
        return

    frame = controller.last_event.cv2img
    annotated = draw_hud(frame, action_name, step_no, agent_info)
    cv2.imshow(WINDOW_NAME, annotated)
    cv2.waitKey(1)


def execute_step(
    controller: Controller,
    action: str,
    step_no: int,
    pddl_rule: str = "",
    delay: float = STEP_DELAY,
    **kwargs: Any,
) -> bool:
    """Bir AI2-THOR aksiyonunu çalıştırır, PDDL durumunu kaydeder ve yavaşça ilerler."""
    event = controller.step(action=action, **kwargs)
    success = bool(event.metadata.get("lastActionSuccess", False))
    agent_info = get_agent_info(controller)

    details = ""
    if not success:
        details = event.metadata.get("errorMessage", "Hata detayı bilinmiyor")
    else:
        pos = agent_info["pos"]
        details = f"x={pos['x']:.2f}, y={pos['y']:.2f}, z={pos['z']:.2f}, yön={agent_info['rot']:.0f}°"

    log_action_status(step_no, action, success, pddl_rule=pddl_rule, details=details)
    update_display(controller, action, step_no, agent_info)

    if delay > 0:
        time.sleep(delay)

    return success


def get_all_objects(controller: Controller) -> List[Dict[str, Any]]:
    return controller.last_event.metadata.get("objects", [])


def find_best_pickup_target(controller: Controller) -> Optional[Dict[str, Any]]:
    """Sahnede alınabilir (pickupable) ve uygun olan en iyi nesneyi bulur."""
    objects = get_all_objects(controller)

    # Önce öncelikli nesneleri ara
    for obj_type in PREFERRED_PICKUP_TYPES:
        for obj in objects:
            if obj.get("objectType") == obj_type and obj.get("pickupable") and not obj.get("isPickedUp"):
                return obj

    # Bulunamazsa herhangi bir pickupable nesne seç
    for obj in objects:
        if obj.get("pickupable") and not obj.get("isPickedUp"):
            return obj

    return None


def approach_object_deliberately(
    controller: Controller,
    target_obj: Dict[str, Any],
    step_counter: List[int],
    delay: float = STEP_DELAY,
) -> bool:
    """GetInteractablePoses ile PDDL interactable ön koşulunu sağlar ve hedefe yönelir."""
    target_id = target_obj["objectId"]
    target_name = target_obj.get("objectType", "Bilinmeyen Nesne")

    print(f"\n>>> Hedefe yaklaşılıyor: {target_name} ({target_id})")

    # 1. AI2-THOR'dan bu nesne için geçerli etkileşim pozisyonlarını al
    event = controller.step(action="GetInteractablePoses", objectId=target_id)
    poses = event.metadata.get("actionReturn") or []

    if not poses:
        print(f"  [UYARI] '{target_name}' için erişilebilir etkileşim pozu bulunamadı.")
        return False

    # Ajanın şu anki konumuna en yakın pozu seç
    agent_pos = controller.last_event.metadata["agent"]["position"]
    best_pose = min(
        poses,
        key=lambda p: (p["x"] - agent_pos["x"]) ** 2 + (p["z"] - agent_pos["z"]) ** 2,
    )

    step_counter[0] += 1
    # PDDL (interactable ?a ?o) ön koşulunu sağlamak için pozisyona ve açıya hizalan
    success = execute_step(
        controller,
        action="TeleportFull",
        step_no=step_counter[0],
        pddl_rule="(interactable ?a ?o) — GetInteractablePoses ile hizalanma",
        delay=delay,
        position={"x": best_pose["x"], "y": best_pose["y"], "z": best_pose["z"]},
        rotation={"x": 0, "y": best_pose["rotation"], "z": 0},
        horizon=best_pose["horizon"],
        standing=best_pose["standing"],
    )
    return success


# ==============================================================================
# DEMO ADIMLARI
# ==============================================================================

def run_slow_walking_demo(controller: Controller, step_counter: List[int], delay: float) -> None:
    """Robotun sakin ve adım adım yürümesini gösteren navigasyon sekansı."""
    log_header("AŞAMA 1: YAVAŞ YÜRÜME VE ÇEVRE GÖZLEMİ (Navigasyon)")
    print("Robot koridorda/mutfakta yavaşça ilerliyor ve etrafını inceliyor...\n")

    # 1. Adım: İleri adım
    step_counter[0] += 1
    execute_step(
        controller,
        action="MoveAhead",
        step_no=step_counter[0],
        pddl_rule="(at-agent ?a ?to), (not (blocked-forward))",
        delay=delay,
    )

    # 2. Adım: Bir adım daha ileri
    step_counter[0] += 1
    execute_step(
        controller,
        action="MoveAhead",
        step_no=step_counter[0],
        pddl_rule="(at-agent ?a ?to)",
        delay=delay,
    )

    # 3. Adım: Sağa dönüp mutfak tezgahına bak
    step_counter[0] += 1
    execute_step(
        controller,
        action="RotateRight",
        step_no=step_counter[0],
        pddl_rule="(facing ?a ?dir)",
        delay=delay,
    )

    # 4. Adım: Bir adım daha ilerle
    step_counter[0] += 1
    execute_step(
        controller,
        action="MoveAhead",
        step_no=step_counter[0],
        pddl_rule="(at-agent ?a ?to)",
        delay=delay,
    )

    # 5. Adım: Başını hafifçe aşağı eğ (masadaki/tezgahtaki nesneleri görmek için)
    step_counter[0] += 1
    execute_step(
        controller,
        action="LookDown",
        step_no=step_counter[0],
        pddl_rule="(camera-horizon ?a 30)",
        delay=delay,
    )


def run_slow_pickup_demo(
    controller: Controller,
    step_counter: List[int],
    delay: float,
) -> Optional[Dict[str, Any]]:
    """PDDL kurallarına tam uyumlu nesne bulma ve tutma (PickupObject) sekansı."""
    log_header("AŞAMA 2: PDDL UYUMLU NESNE TUTMA (PickupObject)")

    target_obj = find_best_pickup_target(controller)
    if not target_obj:
        print("  [HATA] Sahnede alınabilir uygun bir nesne bulunamadı.")
        return None

    target_id = target_obj["objectId"]
    target_name = target_obj.get("objectType", "Nesne")
    print(f"Hedef Nesne Tespit Edildi: {target_name} (ID: {target_id})")

    # Hedefe yaklaş
    if not approach_object_deliberately(controller, target_obj, step_counter, delay=delay):
        print("  [HATA] Hedefe yaklaşılamadı.")
        return None

    # Hedef nesnenin güncel durumunu metadata'dan kontrol et
    current_objs = {o["objectId"]: o for o in get_all_objects(controller)}
    target_now = current_objs.get(target_id, target_obj)
    agent_info = get_agent_info(controller)

    # PDDL Ön Koşul Kontrolleri:
    print("\n--- PDDL Ön Koşul Doğrulaması (wiki/pddl_mappings/PickupObject.md) ---")
    p1 = target_now.get("pickupable", False)
    p2 = agent_info["hand_empty"]
    p3 = target_now.get("visible", False)
    p4 = not target_now.get("isPickedUp", False)

    print(f"  1. (pickupable {target_name}) : {'EVET' if p1 else 'HAYIR'}")
    print(f"  2. (hand-empty robot)        : {'EVET' if p2 else 'HAYIR'}")
    print(f"  3. (visible {target_name})    : {'EVET' if p3 else 'HAYIR'}")
    print(f"  4. (not (holding robot {target_name})) : {'EVET' if p4 else 'HAYIR'}")

    # PickupObject aksiyonu
    step_counter[0] += 1
    success = execute_step(
        controller,
        action="PickupObject",
        step_no=step_counter[0],
        pddl_rule="pre: (pickupable), (hand-empty), (visible), (interactable)",
        delay=delay * 1.5,  # Nesneyi elde görmesi için biraz daha uzun bekle
        objectId=target_id,
    )

    if success:
        print(f"\n>>> BAŞARILI: Robot '{target_name}' nesnesini eline aldı!")
        print("    PDDL Sonucu: (holding robot ?o)=True, (hand-empty robot)=False")
        return target_now
    else:
        print(f"\n>>> BAŞARISIZ: '{target_name}' tutulamadı.")
        return None


def run_held_object_movement_demo(
    controller: Controller,
    held_obj: Dict[str, Any],
    step_counter: List[int],
    delay: float,
) -> None:
    """Nesne elde tutulurken yürüme ve dönme hareketini gösterir."""
    log_header("AŞAMA 3: NESNE ELDEYKEN HAREKET (Taşıma)")
    obj_name = held_obj.get("objectType", "Nesne")
    print(f"Robot elinde '{obj_name}' tutarken yavaşça hareket ediyor...\n")

    # 1. Nesne elde sağa dön
    step_counter[0] += 1
    execute_step(
        controller,
        action="RotateRight",
        step_no=step_counter[0],
        pddl_rule="(holding robot ?o) korunur",
        delay=delay,
    )

    # 2. Nesne elde bir adım geri veya ileri
    step_counter[0] += 1
    execute_step(
        controller,
        action="MoveBack",
        step_no=step_counter[0],
        pddl_rule="(holding robot ?o), (at-agent ?a ?to)",
        delay=delay,
    )

    # 3. Tekrar sola dönerek tezgahı karşına al
    step_counter[0] += 1
    execute_step(
        controller,
        action="RotateLeft",
        step_no=step_counter[0],
        pddl_rule="(facing ?a ?dir)",
        delay=delay,
    )


def run_optional_put_demo(
    controller: Controller,
    held_obj: Dict[str, Any],
    step_counter: List[int],
    delay: float,
) -> bool:
    """İsteğe bağlı: Tutulan nesneyi tezgah veya masaya geri bırakma (PutObject)."""
    log_header("AŞAMA 4: NESNEYİ GERİ BIRAKMA (PutObject)")
    obj_name = held_obj.get("objectType", "Nesne")

    # Yakında bir receptacle (CounterTop veya DiningTable) bul
    objects = get_all_objects(controller)
    receptacle = None
    for obj in objects:
        if obj.get("receptacle") and obj.get("visible") and obj.get("objectId") != held_obj["objectId"]:
            receptacle = obj
            break

    if not receptacle:
        print("  Görüş alanında uygun yüzey (receptacle) bulunamadı; nesne elde tutulmaya devam ediliyor.")
        return False

    rec_name = receptacle.get("objectType", "Yüzey")
    print(f"Uygun Yüzey Bulundu: {rec_name} (ID: {receptacle['objectId']})")

    step_counter[0] += 1
    success = execute_step(
        controller,
        action="PutObject",
        step_no=step_counter[0],
        pddl_rule="pre: (holding ?a ?o), (receptacle ?r), (visible ?r)",
        delay=delay * 1.5,
        objectId=receptacle["objectId"],
        placeStationary=True,
    )

    if success:
        print(f"\n>>> BAŞARILI: '{obj_name}' nesnesi '{rec_name}' üzerine bırakıldı.")
        print("    PDDL Sonucu: (hand-empty robot)=True, (on-surface ?o)=True")
    return success


# ==============================================================================
# ANA PROGRAM (MAIN)
# ==============================================================================

def main() -> None:
    log_header(f"AI2-THOR Simülasyonu Başlatılıyor ({SCENE})")
    print(f"Çözünürlük     : {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"OpenCV Modu    : {'Açık (Pencereli HUD)' if USE_OPENCV else 'Kapalı (Tek Pencere - Unity Native)'}")
    print(f"Adım Gecikmesi : {STEP_DELAY} saniye (Yavaş ve izlenebilir mod)")

    if not USE_OPENCV:
        print("\n[BİLGİ] Çift uygulama karışıklığını önlemek için sadece AI2-THOR Unity penceresi")
        print("       kullanılmaktadır. Ekstra bir tam ekran pencere açılmayacaktır.")

    # Controller'ı başlat
    controller = create_controller(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

    if USE_OPENCV:
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(WINDOW_NAME, SCREEN_WIDTH, SCREEN_HEIGHT)

    step_counter = [0]

    try:
        if verify_agent_position(controller):
            info = get_agent_info(controller)
            pos = info["pos"]
            print(f"\nRobot başarıyla konumlandırıldı -> x={pos['x']:.2f}, y={pos['y']:.2f}, z={pos['z']:.2f}")
        else:
            print("\n[UYARI] Robot konumu doğrulanamadı, varsayılan koordinatla devam ediliyor.")

        # İlk kareyi göster (OpenCV açıksa)
        update_display(controller, "Baslangic", 0, get_agent_info(controller))
        time.sleep(1.0)

        # 1. Aşama: Yavaş Yürüme
        run_slow_walking_demo(controller, step_counter, delay=STEP_DELAY)

        # 2. Aşama: Nesne Tutma (PickupObject)
        held_target = run_slow_pickup_demo(controller, step_counter, delay=STEP_DELAY)

        # 3. Aşama: Nesne Eldeyken Yürüme/Dönme
        if held_target:
            run_held_object_movement_demo(controller, held_target, step_counter, delay=STEP_DELAY)

            # 4. Aşama: Nesneyi Bırakma
            run_optional_put_demo(controller, held_target, step_counter, delay=STEP_DELAY)

        # Simülasyon Tamamlandı Özeti
        log_header("SİMÜLASYON GÖREVİ BAŞARIYLA TAMAMLANDI")
        print("✓ Toplam çalıştırılan adım sayısı :", step_counter[0])
        print("✓ Robot tüm yürüme ve etkileşim hareketlerini tamamladı.")
        print("✓ Pencere açık kalmaya devam ediyor.")
        print("\nSimülasyonu güvenle kapatmak için terminalde ENTER tuşuna basın...")

        # Kapanmadan önce kullanıcının Enter'a basmasını bekle (Aniden kapanma sorununu çözer!)
        if USE_OPENCV:
            while True:
                key = cv2.waitKey(100)
                if key in (27, ord("q"), ord("Q"), 13):  # ESC, Q veya Enter
                    break
        else:
            input()

    except KeyboardInterrupt:
        print("\nKullanıcı tarafından durduruldu.")
    finally:
        print("\nSimülasyon ortamı kapatılıyor...")
        if USE_OPENCV:
            cv2.destroyAllWindows()
        controller.stop()
        print("Simülasyon güvenli şekilde kapatıldı.")


if __name__ == "__main__":
    main()
