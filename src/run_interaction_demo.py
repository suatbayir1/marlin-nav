"""FloorPlan1'de open/close ve pickup/put etkileşimlerini gösteren demo simülasyonu."""

from typing import Any, Callable, Dict, List, Optional

import cv2

from ai2thor.controller import Controller
from src.thor_env import SCENE, WINDOW_NAME, create_controller, get_screen_resolution, verify_agent_position

# FloorPlan1 mutfak sahnesinde sık bulunan nesne tipleri (öncelik sırasıyla)
OPENABLE_TYPES = ("Fridge", "Microwave", "Cabinet", "Drawer")
PICKUPABLE_TYPES = ("Apple", "Potato", "Mug", "Egg", "Knife", "Tomato")
RECEPTACLE_TYPES = ("CounterTop", "DiningTable", "Plate", "SinkBasin")

PDDL_RULES = {
    "OpenObject": "openable, kapalı, visible, interactable",
    "CloseObject": "openable, açık, visible, interactable",
    "PickupObject": "pickupable, el boş, visible, interactable",
    "PutObject": "nesne tutuluyor, geçerli receptacle, visible",
}


def get_objects(controller: Controller) -> List[Dict[str, Any]]:
    return controller.last_event.metadata.get("objects", [])


def find_object(
    objects: List[Dict[str, Any]],
    type_names: tuple[str, ...],
    predicate: Callable[[Dict[str, Any]], bool],
) -> Optional[Dict[str, Any]]:
    for type_name in type_names:
        for obj in objects:
            if obj.get("objectType") == type_name and predicate(obj):
                return obj
    return None


def describe_object(obj: Dict[str, Any]) -> str:
    parts = [obj.get("objectType", "?"), obj.get("objectId", "?")]
    if obj.get("openable"):
        parts.append(f"isOpen={obj.get('isOpen')}")
    if obj.get("pickupable"):
        parts.append(f"isPickedUp={obj.get('isPickedUp')}")
    if obj.get("receptacle"):
        parts.append("receptacle=True")
    return " | ".join(parts)


def approach_object(controller: Controller, object_id: str) -> bool:
    """GetInteractablePoses + TeleportFull ile PDDL interactable ön koşulunu sağlar."""
    event = controller.step(action="GetInteractablePoses", objectId=object_id)
    poses = event.metadata.get("actionReturn") or []
    if not poses:
        return False

    pose = poses[0]
    event = controller.step(
        action="TeleportFull",
        position={"x": pose["x"], "y": pose["y"], "z": pose["z"]},
        rotation={"x": 0, "y": pose["rotation"], "z": 0},
        horizon=pose["horizon"],
        standing=pose["standing"],
    )
    return bool(event.metadata.get("lastActionSuccess"))


def run_action(
    controller: Controller,
    action: str,
    label: str,
    **kwargs: Any,
) -> bool:
    pddl_hint = PDDL_RULES.get(action, "")
    print(f"\n[{label}] {action}  (PDDL: {pddl_hint})")
    if kwargs:
        print(f"  parametreler: {kwargs}")

    event = controller.step(action=action, **kwargs)
    success = bool(event.metadata.get("lastActionSuccess"))
    if success:
        print("  sonuç: BAŞARILI")
    else:
        print(f"  sonuç: BAŞARISIZ — {event.metadata.get('errorMessage', 'bilinmeyen hata')}")
    return success


def get_object_state(controller: Controller, object_id: str) -> Optional[Dict[str, Any]]:
    for obj in get_objects(controller):
        if obj.get("objectId") == object_id:
            return obj
    return None


def pause_and_show(controller: Controller, message: str) -> None:
    print(f"\n>>> {message}")
    cv2.imshow(WINDOW_NAME, controller.last_event.cv2img)
    cv2.waitKey(0)


def setup_window(width: int = 1024, height: int = 768) -> None:
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, width, height)


def run_open_close_demo(controller: Controller) -> bool:
    objects = get_objects(controller)
    target = find_object(
        objects,
        OPENABLE_TYPES,
        lambda o: o.get("openable") and not o.get("isOpen"),
    )
    if target is None:
        print("Açılabilir kapalı nesne bulunamadı.")
        return False

    print(f"\n--- Açı/Kapa demosu ---\nHedef: {describe_object(target)}")
    if not approach_object(controller, target["objectId"]):
        print("Hedefe yaklaşılamadı (GetInteractablePoses boş).")
        return False

    pause_and_show(controller, "Kapalı nesne — OpenObject öncesi")

    if not run_action(controller, "OpenObject", "1/2", objectId=target["objectId"]):
        return False

    opened = get_object_state(controller, target["objectId"])
    print(f"  durum: {describe_object(opened) if opened else 'bulunamadı'}")
    pause_and_show(controller, "Nesne açıldı — CloseObject öncesi")

    if not run_action(controller, "CloseObject", "2/2", objectId=target["objectId"]):
        return False

    closed = get_object_state(controller, target["objectId"])
    print(f"  durum: {describe_object(closed) if closed else 'bulunamadı'}")
    pause_and_show(controller, "Nesne tekrar kapandı")
    return True


def run_pickup_put_demo(controller: Controller) -> bool:
    objects = get_objects(controller)
    pickup_target = find_object(
        objects,
        PICKUPABLE_TYPES,
        lambda o: o.get("pickupable") and not o.get("isPickedUp"),
    )
    if pickup_target is None:
        print("Alınabilir nesne bulunamadı.")
        return False

    print(f"\n--- Pickup/Put demosu ---\nHedef nesne: {describe_object(pickup_target)}")
    if not approach_object(controller, pickup_target["objectId"]):
        print("Nesneye yaklaşılamadı.")
        return False

    pause_and_show(controller, "PickupObject öncesi — nesne yerde")

    if not run_action(controller, "PickupObject", "1/2", objectId=pickup_target["objectId"]):
        return False

    held = get_object_state(controller, pickup_target["objectId"])
    print(f"  durum: {describe_object(held) if held else 'bulunamadı'}")
    pause_and_show(controller, "Nesne elde — PutObject için receptacle aranıyor")

    objects = get_objects(controller)
    receptacle = find_object(
        objects,
        RECEPTACLE_TYPES,
        lambda o: o.get("receptacle") and o.get("objectId") != pickup_target["objectId"],
    )
    if receptacle is None:
        print("Uygun receptacle bulunamadı.")
        return False

    print(f"Receptacle: {describe_object(receptacle)}")
    if not approach_object(controller, receptacle["objectId"]):
        print("Receptacle'a yaklaşılamadı.")
        return False

    pause_and_show(controller, "PutObject öncesi — receptacle görüş alanında")

    if not run_action(
        controller,
        "PutObject",
        "2/2",
        objectId=receptacle["objectId"],
        placeStationary=True,
    ):
        return False

    placed = get_object_state(controller, pickup_target["objectId"])
    print(f"  durum: {describe_object(placed) if placed else 'bulunamadı'}")
    pause_and_show(controller, "Nesne receptacle üzerine yerleştirildi")
    return True


def main() -> None:
    width, height = get_screen_resolution()
    print(f"Ekran çözünürlüğü: {width}x{height}")
    print(f"=== Etkileşim Demosu — {SCENE} ===")
    print("PDDL ön koşulları: wiki/pddl_mappings/ (visible, interactable, vb.)")

    controller = create_controller(width, height)
    setup_window()

    try:
        if verify_agent_position(controller):
            agent = controller.last_event.metadata["agent"]
            pos = agent["position"]
            print(
                f"Robot konumlandı — x={pos['x']:.2f}, y={pos['y']:.2f}, z={pos['z']:.2f}"
            )
        else:
            print("Uyarı: Robot konumu doğrulanamadı.")

        pause_and_show(controller, "Demo başlıyor — her adımda bir tuşa basın")

        open_ok = run_open_close_demo(controller)
        pickup_ok = run_pickup_put_demo(controller)

        print("\n=== Demo Özeti ===")
        print(f"  Open/Close : {'OK' if open_ok else 'ATLANDI/BAŞARISIZ'}")
        print(f"  Pickup/Put : {'OK' if pickup_ok else 'ATLANDI/BAŞARISIZ'}")

        input("\nSimülasyonu kapatmak için Enter'a basın...")
    finally:
        cv2.destroyAllWindows()
        controller.stop()
        print("Simülasyon güvenli şekilde kapatıldı.")


if __name__ == "__main__":
    main()
