"""
AI2-THOR — Adım Adım (Döngü Tabanlı) Navigasyon ve Nesne Tutma Plan Executor.

Mimari:
  1. Ortam state'inden hedef nesnenin (Apple) anlık konumu (x, y, z) okunur.
  2. Robotun anlık konumu ve yönü sürekli state'ten takip edilir.
  3. Robot hedefe ışınlanmaz; döngü içerisinde adım adım:
     - Sağa dön (RotateRight)
     - Sola dön (RotateLeft)
     - Düz yürü (MoveAhead)
     komutlarıyla engellerden kaçınarak nesneye yaklaşır.
  4. Tutma mesafesine ve açısına geldikten sonra nesneyi alır (PickupObject).
  5. Başlangıç konumuna aynı şekilde adım adım geri döner.
"""

import collections
import math
from typing import Any, Dict, List, Optional, Tuple

import cv2
from ai2thor.controller import Controller

from src.thor_env import SCENE, WINDOW_NAME

# ==============================================================================
# AYARLAR
# ==============================================================================
AGENT_MODE     = "stretch"    # Fiziksel Stretch robotu
STEP_DELAY_MS  = 650          # Her adım arasındaki bekleme (ms) — canlı takip
NEARBY_DIST_M  = 3.5          # State taramasında listelenecek yarıçap

# Dış kamera — Yakın ve üstten robotu net görecek açı
CAM_BACK  = 1.0   # Robotun arkasına uzaklık (metre)
CAM_UP    = 1.3   # Robotun üstüne yükseklik (metre)
CAM_TILT  = 38    # Aşağı eğim açısı (derece)

# ==============================================================================
# PLAN TANIMI (Dışarıdan verilen üst düzey plan)
# ==============================================================================
PLAN: List[Dict[str, Any]] = [
    {"action": "navigate_to",   "target": "Apple"},
    {"action": "pickup_object", "target": "Apple"},
    {"action": "return_to_start"},
]


# ==============================================================================
# KAMERA VE CANLI GÖRÜNTÜ
# ==============================================================================

def cam_pose(pos: dict, rot_y: float) -> dict:
    """Robotun anlık konumuna göre yakın-üst dış kamera pozisyonunu hesaplar."""
    rad = math.radians(rot_y - 35)
    return {
        "position": dict(
            x=pos["x"] - CAM_BACK * math.sin(rad),
            y=pos["y"] + CAM_UP,
            z=pos["z"] - CAM_BACK * math.cos(rad),
        ),
        "rotation": dict(x=CAM_TILT, y=rot_y - 30, z=0),
    }


def update_camera(controller: Controller) -> None:
    """Dış kamerayı robotun güncel state konumuna taşır."""
    agent = controller.last_event.metadata["agent"]
    pose  = cam_pose(agent["position"], agent["rotation"]["y"])
    controller.step(action="UpdateThirdPartyCamera", thirdPartyCameraId=0, **pose)


def show(controller: Controller, label: str = "") -> None:
    """Dış kamera görüntüsünü OpenCV penceresinde anında render eder."""
    frames = controller.last_event.third_party_camera_frames
    if not frames:
        return
    frame = cv2.cvtColor(frames[0], cv2.COLOR_RGB2BGR)
    if label:
        cv2.putText(frame, label, (20, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.70, (0, 255, 255), 2)
    cv2.imshow(WINDOW_NAME, frame)
    cv2.waitKey(1)


def live_wait(ms: int) -> bool:
    """Pencere donmasını engelleyen canlı olay döngüsü. False → çıkış."""
    waited = 0
    while waited < ms:
        key = cv2.waitKey(30) & 0xFF
        if key in (27, ord("q"), ord("Q")):
            return False
        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            return False
        waited += 30
    return True


# ==============================================================================
# ORTAM STATE VE NESNE YÖNETİMİ
# ==============================================================================

def get_agent_state(controller: Controller) -> Tuple[Dict[str, float], float, float]:
    """State'ten robotun anlık (x, y, z) pozisyonunu, rotasyonunu ve horizon açısını döner."""
    agent = controller.last_event.metadata["agent"]
    pos = agent["position"]
    rot = round(agent["rotation"]["y"]) % 360
    horizon = round(agent.get("cameraHorizon", 0.0))
    return pos, rot, horizon


def find_object_by_type(controller: Controller, obj_type: str) -> Optional[dict]:
    """State içerisinden verilen tipte ilk nesneyi tüm alanlarıyla döner."""
    for obj in controller.last_event.metadata.get("objects", []):
        if obj.get("objectType") == obj_type:
            return obj
    return None


def print_nearby_objects(controller: Controller, max_dist: float = NEARBY_DIST_M) -> None:
    """Robotun çevresindeki nesneleri state'ten okuyup konsola döker."""
    agent_pos, _, _ = get_agent_state(controller)
    objects = controller.last_event.metadata.get("objects", [])

    nearby = []
    for obj in objects:
        p = obj.get("position")
        if not p:
            continue
        dist = math.sqrt((p["x"] - agent_pos["x"])**2 + (p["z"] - agent_pos["z"])**2)
        if dist <= max_dist:
            nearby.append({
                "type":        obj.get("objectType", "?"),
                "dist":        round(dist, 2),
                "visible":     obj.get("visible", False),
                "pickupable":  obj.get("pickupable", False),
                "openable":    obj.get("openable", False),
                "receptacle":  obj.get("receptacle", False),
            })

    nearby.sort(key=lambda x: x["dist"])
    print(f"\n{'='*70}")
    print(f"  ORTAM STATE: YAKINDAKİ NESNELER ({len(nearby)} adet, {max_dist}m çap)")
    print(f"{'='*70}")
    print(f"  {'Tip':<20} {'Mesafe':>7}  {'Görünür':>8}  {'Alınabilir':>11}  {'Yüzey':>6}")
    print(f"  {'-'*60}")
    for o in nearby:
        print(
            f"  {o['type']:<20} {o['dist']:>6.2f}m"
            f"  {'EVET' if o['visible'] else 'HAYIR':>8}"
            f"  {'EVET' if o['pickupable'] else 'HAYIR':>11}"
            f"  {'EVET' if o['receptacle'] else 'HAYIR':>6}"
        )
    print(f"{'='*70}\n")


# ==============================================================================
# ADIM ADIM NAVİGASYON (IZGARA BFS + DÖNGÜ HAREKETLERİ)
# ==============================================================================

def build_reachable_graph(positions: List[dict]) -> Tuple[List[Tuple[float, float]], Dict[Tuple[float, float], List[Tuple[float, float]]]]:
    """ReachablePositions ızgarasını ayrıştırıp komşuluk grafı oluşturur."""
    pts = list({(round(p["x"], 2), round(p["z"], 2)) for p in positions})
    graph: Dict[Tuple[float, float], List[Tuple[float, float]]] = {pt: [] for pt in pts}

    for i, p1 in enumerate(pts):
        for j in range(i + 1, len(pts)):
            p2 = pts[j]
            dx = abs(p1[0] - p2[0])
            dz = abs(p1[1] - p2[1])
            # AI2-THOR 0.25m ızgara komşuluk toleransı
            if (abs(dx - 0.25) < 0.04 and dz < 0.04) or (abs(dz - 0.25) < 0.04 and dx < 0.04):
                graph[p1].append(p2)
                graph[p2].append(p1)

    return pts, graph


def find_bfs_path(
    graph: Dict[Tuple[float, float], List[Tuple[float, float]]],
    pts: List[Tuple[float, float]],
    start: Tuple[float, float],
    goal: Tuple[float, float],
) -> Optional[List[Tuple[float, float]]]:
    """Başlangıç ve hedef koordinatları arasında engelsiz en kısa yolu bulur."""
    c_start = min(pts, key=lambda p: (p[0] - start[0])**2 + (p[1] - start[1])**2)
    c_goal  = min(pts, key=lambda p: (p[0] - goal[0])**2 + (p[1] - goal[1])**2)

    if c_start == c_goal:
        return [c_start]

    queue = collections.deque([[c_start]])
    visited = {c_start}

    while queue:
        path = queue.popleft()
        curr = path[-1]
        for neighbor in graph.get(curr, []):
            if neighbor == c_goal:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None


def get_required_rotation(from_pt: Tuple[float, float], to_pt: Tuple[float, float]) -> Optional[int]:
    """Bir ızgara noktasından diğerine gitmek için gereken pusula açısı."""
    dx = to_pt[0] - from_pt[0]
    dz = to_pt[1] - from_pt[1]
    if dx > 0.1:
        return 90    # Doğu (+X)
    if dx < -0.1:
        return 270   # Batı (-X)
    if dz > 0.1:
        return 0     # Kuzey (+Z)
    if dz < -0.1:
        return 180   # Güney (-Z)
    return None


def step_rotate_to(controller: Controller, target_rot: int, context_label: str) -> bool:
    """Robotu istenen açıya RotateRight/RotateLeft komutlarıyla adım adım döndürür."""
    while True:
        _, curr_rot, _ = get_agent_state(controller)
        diff = (target_rot - curr_rot) % 360
        if diff == 0:
            return True

        if diff == 90 or diff == 180:
            action = "RotateRight"
            desc = "Sağa dön"
        else:
            action = "RotateLeft"
            desc = "Sola dön"

        event = controller.step(action=action)
        if not event.metadata.get("lastActionSuccess", False):
            print(f"    [HATA] Dönüş başarısız: {action}")
            return False

        update_camera(controller)
        _, new_rot, _ = get_agent_state(controller)
        lbl = f"{context_label}: {desc} -> {new_rot}°"
        print(f"    ↳ {desc} ({action}) -> State Güncel Yön: {new_rot}°")
        show(controller, lbl)
        if not live_wait(STEP_DELAY_MS):
            return False


def navigate_step_by_step(
    controller: Controller,
    goal_pos: Tuple[float, float],
    goal_rot: Optional[int],
    goal_horizon: Optional[int],
    reachable_pts: List[Tuple[float, float]],
    graph: Dict[Tuple[float, float], List[Tuple[float, float]]],
    task_name: str,
) -> bool:
    """
    Hedef koordinata adım adım (RotateLeft/Right + MoveAhead) döngüsüyle gider.
    Işınlanma (Teleport) KESİNLİKLE KULLANILMAZ.
    """
    pos, rot, _ = get_agent_state(controller)
    curr_pt = (round(pos["x"], 2), round(pos["z"], 2))

    path = find_bfs_path(graph, reachable_pts, curr_pt, goal_pos)
    if not path or len(path) == 0:
        print(f"    [HATA] Hedefe giden engelsiz bir yol bulunamadı.")
        return False

    print(f"    Rota hesaplandı: {len(path)} ızgara adımı. Döngü yürütülüyor...")

    # Yol üzerindeki her hücreye tek tek yürü
    for i in range(len(path) - 1):
        p_from = path[i]
        p_to   = path[i + 1]

        needed_rot = get_required_rotation(p_from, p_to)
        if needed_rot is not None:
            if not step_rotate_to(controller, needed_rot, f"{task_name} [Adım {i+1}]"):
                return False

        # Düz adım at
        event = controller.step(action="MoveAhead")
        update_camera(controller)
        new_pos, new_rot, _ = get_agent_state(controller)

        if not event.metadata.get("lastActionSuccess", False):
            print(f"    [ENGEL] MoveAhead engellendi! x={new_pos['x']:.2f}, z={new_pos['z']:.2f}")
            # Küçük toleransla hedefe çok yakınsak devam edebiliriz
            if math.sqrt((new_pos["x"] - goal_pos[0])**2 + (new_pos["z"] - goal_pos[1])**2) < 0.4:
                break
            return False

        lbl = f"{task_name}: Düz Yürü (MoveAhead) -> x={new_pos['x']:.2f}, z={new_pos['z']:.2f}"
        print(f"    ↳ Düz yürü (MoveAhead) -> State Konum: x={new_pos['x']:.2f}, z={new_pos['z']:.2f}")
        show(controller, lbl)

        if not live_wait(STEP_DELAY_MS):
            return False

    # Hedef noktaya varıldığında istenen hedef açıya dön (örn: nesnenin durduğu masa yönüne)
    if goal_rot is not None:
        if not step_rotate_to(controller, goal_rot, f"{task_name} [Hedefe Hizalan]"):
            return False

    # Gerekirse kamerayı aşağı eğ (masadaki nesneyi doğrudan görmek için)
    if goal_horizon is not None and goal_horizon > 0:
        _, _, curr_h = get_agent_state(controller)
        if curr_h < goal_horizon:
            deg = goal_horizon - curr_h
            controller.step(action="LookDown", degrees=deg)
            update_camera(controller)
            print(f"    ↳ Aşağı bak (LookDown degrees={deg}) -> Tezgah/Masa odağı")
            show(controller, f"{task_name}: LookDown {deg}°")
            live_wait(STEP_DELAY_MS)

    return True


# ==============================================================================
# PLAN YÜRÜTÜCÜ (EXECUTOR)
# ==============================================================================

def execute_plan(
    controller: Controller,
    plan: List[Dict[str, Any]],
    start_pos: Dict[str, float],
    start_rot: float,
    reachable_pts: List[Tuple[float, float]],
    graph: Dict[Tuple[float, float], List[Tuple[float, float]]],
) -> None:
    """Planı adım adım yorumlayıp çalıştırır."""
    print(f"\n{'='*70}")
    print(f"  DIŞARIDAN GELEN PLAN ÇALIŞTIRILIYOR ({len(plan)} Adım)")
    print(f"{'='*70}")

    for step_idx, step in enumerate(plan, 1):
        action = step.get("action", "")
        target = step.get("target", "")
        print(f"\n>>> [Plan Adımı {step_idx}/{len(plan)}] Aksiyon: '{action}' | Hedef: '{target or '—'}'")

        # ----------------------------------------------------------------------
        # 1. NAVIGATE_TO (Nesneye Adım Adım Yaklaşma)
        # ----------------------------------------------------------------------
        if action == "navigate_to":
            obj = find_object_by_type(controller, target)
            if not obj:
                print(f"  [HATA] Sahnede '{target}' nesnesi bulunamadı!")
                continue

            obj_pos = obj["position"]
            robot_pos, robot_rot, _ = get_agent_state(controller)
            dist = math.sqrt((obj_pos["x"] - robot_pos["x"])**2 + (obj_pos["z"] - robot_pos["z"])**2)

            print(f"  [STATE BİLGİSİ]")
            print(f"    Hedef Nesne  : {obj['objectType']} (ID: {obj['objectId']})")
            print(f"    Nesne Konumu : x={obj_pos['x']:.2f}, y={obj_pos['y']:.2f}, z={obj_pos['z']:.2f}")
            print(f"    Robot Konumu : x={robot_pos['x']:.2f}, y={robot_pos['y']:.2f}, z={robot_pos['z']:.2f} (Yön: {robot_rot}°)")
            print(f"    Mesafe       : {dist:.2f} metre")

            # Etkileşim pozisyonlarını al
            p_event = controller.step(action="GetInteractablePoses", objectId=obj["objectId"])
            poses = p_event.metadata.get("actionReturn") or []

            if poses:
                best = min(poses, key=lambda p: (p["x"] - robot_pos["x"])**2 + (p["z"] - robot_pos["z"])**2)
                target_pt = (round(best["x"], 2), round(best["z"], 2))
                target_heading = round(best["rotation"]) % 360
                target_horizon = round(best.get("horizon", 30))
            else:
                # Yedek: En yakın erişilebilir ızgara noktası
                best_pt = min(reachable_pts, key=lambda p: (p[0] - obj_pos["x"])**2 + (p[1] - obj_pos["z"])**2)
                target_pt = best_pt
                # Nesneye doğru açı
                deg = math.degrees(math.atan2(obj_pos["x"] - best_pt[0], obj_pos["z"] - best_pt[1])) % 360
                target_heading = int(round(deg / 90.0) * 90) % 360
                target_horizon = 30

            print(f"  Hedef Navigasyon Koordinatı: x={target_pt[0]:.2f}, z={target_pt[1]:.2f}, Yön={target_heading}°")
            ok = navigate_step_by_step(
                controller,
                goal_pos=target_pt,
                goal_rot=target_heading,
                goal_horizon=target_horizon,
                reachable_pts=reachable_pts,
                graph=graph,
                task_name=f"Yaklaş ({target})",
            )
            print(f"  Sonuç: {'✓ HEDEFE VARILDI' if ok else '✗ YAKLAŞMA BAŞARISIZ'}")

        # ----------------------------------------------------------------------
        # 2. PICKUP_OBJECT (Nesneyi Tutma)
        # ----------------------------------------------------------------------
        elif action == "pickup_object":
            obj = find_object_by_type(controller, target)
            if not obj:
                print(f"  [HATA] '{target}' nesnesi bulunamadı!")
                continue

            r_pos, r_rot, r_h = get_agent_state(controller)
            print(f"  Robot anlık konumu: x={r_pos['x']:.2f}, z={r_pos['z']:.2f}, Yön={r_rot}°, Horizon={r_h}°")
            print(f"  Nesne durumu: visible={obj.get('visible')}, pickupable={obj.get('pickupable')}")

            # Nesneyi al
            p_event = controller.step(action="PickupObject", objectId=obj["objectId"])
            success = p_event.metadata.get("lastActionSuccess", False)

            if success:
                print(f"  ✓ BAŞARILI: '{target}' robot tarafından tutuldu!")
                update_camera(controller)
                show(controller, f"TUTULDU: {target} elinde!")
            else:
                err = p_event.metadata.get("errorMessage", "Bilinmeyen hata")
                print(f"  ✗ BAŞARISIZ: Nesne tutulamadı ({err})")
                # Görüş mesafesi için forceAction yedeği (fiziksel etkileşim toleransı)
                retry = controller.step(action="PickupObject", objectId=obj["objectId"], forceAction=True)
                if retry.metadata.get("lastActionSuccess", False):
                    print(f"  ✓ (Tolerans ile) '{target}' robot tarafından tutuldu!")
                    update_camera(controller)
                    show(controller, f"TUTULDU: {target} (Elde)")

            live_wait(STEP_DELAY_MS)

        # ----------------------------------------------------------------------
        # 3. RETURN_TO_START (Başlangıç Konumuna Adım Adım Dönüş)
        # ----------------------------------------------------------------------
        elif action == "return_to_start":
            start_pt = (round(start_pos["x"], 2), round(start_pos["z"], 2))
            start_heading = int(round(start_rot)) % 360
            print(f"  Başlangıç noktasına adım adım dönülüyor: x={start_pt[0]:.2f}, z={start_pt[1]:.2f}, Yön={start_heading}°")

            ok = navigate_step_by_step(
                controller,
                goal_pos=start_pt,
                goal_rot=start_heading,
                goal_horizon=0,  # Horizon'ı düzelt
                reachable_pts=reachable_pts,
                graph=graph,
                task_name="Geri Dön",
            )
            print(f"  Sonuç: {'✓ BAŞLANGIÇ NOKTASINA DÖNÜLDÜ' if ok else '✗ DÖNÜŞ BAŞARISIZ'}")

        else:
            print(f"  [UYARI] Desteklenmeyen plan aksiyonu: {action}")

    print(f"\n{'='*70}")
    print("  TÜM PLAN ADIMLARI TAMAMLANDI")
    print(f"{'='*70}\n")


# ==============================================================================
# ANA PROGRAM
# ==============================================================================

def main() -> None:
    print(f"=== AI2-THOR Adım Adım Navigasyon & Plan Executor — {SCENE} ===\n")

    # 1. Controller başlat
    controller = Controller(
        scene=SCENE,
        agentMode=AGENT_MODE,
        width=1024,
        height=768,
        visibilityDistance=1.5,
        gridSize=0.25,
        snapToGrid=True,
        rotateStepDegrees=90,
        fieldOfView=90,
    )

    # 2. Başlangıç state'ini kaydet
    start_pos, start_rot, _ = get_agent_state(controller)
    print(f"Robot Başlangıç State -> Konum: x={start_pos['x']:.2f}, z={start_pos['z']:.2f} | Yön: {start_rot:.0f}°")

    # 3. Ortam State: Nesneleri konsola yazdır
    print_nearby_objects(controller)

    # 4. Navigasyon için erişilebilir noktaları ve komşuluk grafını hazırla
    r_event = controller.step(action="GetReachablePositions")
    reachable_positions = r_event.metadata.get("actionReturn") or []
    reachable_pts, graph = build_reachable_graph(reachable_positions)
    print(f"Engelsiz Navigasyon Haritası: {len(reachable_pts)} ızgara hücresi hazırlandı.")

    # 5. Dış kamerayı ekle (yakın, üstten bakış)
    pose = cam_pose(start_pos, start_rot)
    cam_event = controller.step(
        action="AddThirdPartyCamera",
        fieldOfView=75,
        **pose,
    )
    if not cam_event.metadata.get("lastActionSuccess", False):
        print(f"[HATA] Dış kamera eklenemedi: {cam_event.metadata.get('errorMessage')}")
        controller.stop()
        return

    # 6. Canlı OpenCV penceresini hazırla
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, 1024, 768)
    show(controller, "Baslangic Konumu")

    if not live_wait(1200):
        controller.stop()
        return

    # 7. Planı yazdır ve döngü tabanlı çalıştır
    print("Yürütülecek Plan:")
    for i, step in enumerate(PLAN, 1):
        print(f"  {i}. {step}")

    execute_plan(
        controller=controller,
        plan=PLAN,
        start_pos=start_pos,
        start_rot=start_rot,
        reachable_pts=reachable_pts,
        graph=graph,
    )

    # 8. Bitiş ekranı
    show(controller, "Gorev Bitti — Cikis icin q / ESC")
    print("\nProgram tamamlandı. Kapatmak için pencere üzerindeyken 'q' veya ESC tuşuna basın...")
    live_wait(300_000)

    cv2.destroyAllWindows()
    controller.stop()
    print("Simülasyon başarıyla kapatıldı.")


if __name__ == "__main__":
    main()
