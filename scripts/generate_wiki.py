#!/usr/bin/env python3
"""Generate wiki/ai2thor_api and wiki/pddl_mappings from action definitions."""

from pathlib import Path
from datetime import date
import re

ROOT = Path(__file__).resolve().parent.parent
WIKI_API = ROOT / "wiki" / "ai2thor_api"
WIKI_PDDL = ROOT / "wiki" / "pddl_mappings"

ACTIONS = {
    # Navigation
    "MoveAhead": {
        "category": "navigation",
        "source": "navigation.md",
        "description": "Ajanı ileri yönde (baktığı yöne) hareket ettirir.",
        "params": [("moveMagnitude", "Optional[float]", False, "None", "gridSize varsayılanını geçersiz kılar (metre).")],
        "example": 'controller.step(action="MoveAhead", moveMagnitude=None)',
        "preconditions": ["Ajanın önünde engel olmamalı.", "snapToGrid=True ise grid noktasına hizalanır."],
        "effects": ["Ajan pozisyonu güncellenir.", "Tutulan nesnenin pozisyonu varsayılan konuma sıfırlanır."],
        "pddl_action": "move-ahead",
        "pddl_params": [("?a - agent"), ("?from - location"), ("?to - location")],
        "pddl_pre": ["(at-agent ?a ?from)", "(adjacent-forward ?from ?to)", "(hand-empty ?a)", "(not (blocked-forward ?from))"],
        "pddl_eff": ["(not (at-agent ?a ?from))", "(at-agent ?a ?to)"],
        "query": False,
    },
    "MoveBack": {
        "category": "navigation",
        "source": "navigation.md",
        "description": "Ajanı geri yönde hareket ettirir.",
        "params": [("moveMagnitude", "Optional[float]", False, "None", "Hareket mesafesi (metre).")],
        "example": 'controller.step("MoveBack")',
        "preconditions": ["Arkada engel olmamalı."],
        "effects": ["Ajan pozisyonu güncellenir."],
        "pddl_action": "move-back",
        "pddl_params": [("?a - agent"), ("?from - location"), ("?to - location")],
        "pddl_pre": ["(at-agent ?a ?from)", "(adjacent-back ?from ?to)", "(not (blocked-back ?from))"],
        "pddl_eff": ["(not (at-agent ?a ?from))", "(at-agent ?a ?to)"],
        "query": False,
    },
    "MoveLeft": {
        "category": "navigation",
        "source": "navigation.md",
        "description": "Ajanı sola (göreli) hareket ettirir.",
        "params": [("moveMagnitude", "Optional[float]", False, "None", "Hareket mesafesi (metre).")],
        "example": 'controller.step("MoveLeft")',
        "preconditions": ["Solda engel olmamalı."],
        "effects": ["Ajan pozisyonu güncellenir."],
        "pddl_action": "move-left",
        "pddl_params": [("?a - agent"), ("?from - location"), ("?to - location")],
        "pddl_pre": ["(at-agent ?a ?from)", "(adjacent-left ?from ?to)", "(not (blocked-left ?from))"],
        "pddl_eff": ["(not (at-agent ?a ?from))", "(at-agent ?a ?to)"],
        "query": False,
    },
    "MoveRight": {
        "category": "navigation",
        "source": "navigation.md",
        "description": "Ajanı sağa (göreli) hareket ettirir.",
        "params": [("moveMagnitude", "Optional[float]", False, "None", "Hareket mesafesi (metre).")],
        "example": 'controller.step("MoveRight")',
        "preconditions": ["Sağda engel olmamalı."],
        "effects": ["Ajan pozisyonu güncellenir."],
        "pddl_action": "move-right",
        "pddl_params": [("?a - agent"), ("?from - location"), ("?to - location")],
        "pddl_pre": ["(at-agent ?a ?from)", "(adjacent-right ?from ?to)", "(not (blocked-right ?from))"],
        "pddl_eff": ["(not (at-agent ?a ?from))", "(at-agent ?a ?to)"],
        "query": False,
    },
    "RotateRight": {
        "category": "navigation",
        "source": "navigation.md",
        "description": "Ajanın gövde yaw rotasyonunu sağa çevirir.",
        "params": [("degrees", "Optional[float]", False, "None", "rotateStepDegrees varsayılanını geçersiz kılar.")],
        "example": 'controller.step(action="RotateRight", degrees=None)',
        "preconditions": [],
        "effects": ["Ajan rotasyonu güncellenir.", "Tutulan nesne rotasyonu sıfırlanır."],
        "pddl_action": "rotate-right",
        "pddl_params": [("?a - agent"), ("?o - orientation"), ("?n - orientation")],
        "pddl_pre": ["(facing ?a ?o)", "(rotate-right ?o ?n)"],
        "pddl_eff": ["(not (facing ?a ?o))", "(facing ?a ?n)"],
        "query": False,
    },
    "RotateLeft": {
        "category": "navigation",
        "source": "navigation.md",
        "description": "Ajanın gövde yaw rotasyonunu sola çevirir.",
        "params": [("degrees", "Optional[float]", False, "None", "Dönüş açısı (derece).")],
        "example": 'controller.step("RotateLeft")',
        "preconditions": [],
        "effects": ["Ajan rotasyonu güncellenir."],
        "pddl_action": "rotate-left",
        "pddl_params": [("?a - agent"), ("?o - orientation"), ("?n - orientation")],
        "pddl_pre": ["(facing ?a ?o)", "(rotate-left ?o ?n)"],
        "pddl_eff": ["(not (facing ?a ?o))", "(facing ?a ?n)"],
        "query": False,
    },
    "LookUp": {
        "category": "navigation",
        "source": "navigation.md",
        "description": "Kameranın pitch açısını yukarı artırır ([-30, 60] aralığında sınırlı).",
        "params": [("degrees", "float", False, "30", "Yukarı bakış açısı (>0).")],
        "example": 'controller.step(action="LookUp", degrees=30)',
        "preconditions": ["horizon < 60 olmalı."],
        "effects": ["cameraHorizon azalır (yukarı bakış)."],
        "pddl_action": "look-up",
        "pddl_params": [("?a - agent"), ("?h - horizon"), ("?nh - horizon")],
        "pddl_pre": ["(camera-horizon ?a ?h)", "(look-up ?h ?nh)"],
        "pddl_eff": ["(not (camera-horizon ?a ?h))", "(camera-horizon ?a ?nh)"],
        "query": False,
    },
    "LookDown": {
        "category": "navigation",
        "source": "navigation.md",
        "description": "Kameranın pitch açısını aşağı artırır.",
        "params": [("degrees", "float", False, "30", "Aşağı bakış açısı (>0).")],
        "example": 'controller.step("LookDown")',
        "preconditions": ["horizon > -30 olmalı."],
        "effects": ["cameraHorizon artar (aşağı bakış)."],
        "pddl_action": "look-down",
        "pddl_params": [("?a - agent"), ("?h - horizon"), ("?nh - horizon")],
        "pddl_pre": ["(camera-horizon ?a ?h)", "(look-down ?h ?nh)"],
        "pddl_eff": ["(not (camera-horizon ?a ?h))", "(camera-horizon ?a ?nh)"],
        "query": False,
    },
    "Crouch": {
        "category": "navigation",
        "source": "navigation.md",
        "description": "Ajanı ayakta duruştan çömelme pozisyonuna geçirir (~0.22m kısalır).",
        "params": [],
        "example": 'controller.step(action="Crouch")',
        "preconditions": ["Ajan ayakta olmalı (isStanding=True)."],
        "effects": ["isStanding=False"],
        "pddl_action": "crouch",
        "pddl_params": [("?a - agent")],
        "pddl_pre": ["(standing ?a)"],
        "pddl_eff": ["(not (standing ?a))", "(crouching ?a)"],
        "query": False,
    },
    "Stand": {
        "category": "navigation",
        "source": "navigation.md",
        "description": "Ajanı çömelme pozisyonundan ayakta duruşa geçirir.",
        "params": [],
        "example": 'controller.step(action="Stand")',
        "preconditions": ["Ajan çömelmiş olmalı."],
        "effects": ["isStanding=True"],
        "pddl_action": "stand",
        "pddl_params": [("?a - agent")],
        "pddl_pre": ["(crouching ?a)"],
        "pddl_eff": ["(not (crouching ?a))", "(standing ?a)"],
        "query": False,
    },
    "Teleport": {
        "category": "navigation",
        "source": "navigation.md",
        "description": "Ajanın pozunu tek adımda belirtilen konuma ayarlar. Belirtilmeyen DOF'lar korunur.",
        "params": [
            ("position", "dict", False, "None", "Global (x,y,z) pozisyon."),
            ("rotation", "dict", False, "None", "Gövde yaw rotasyonu."),
            ("horizon", "float", False, "None", "Kamera pitch ([-30, 60])."),
            ("standing", "bool", False, "None", "Ayakta/çömelmiş durumu."),
        ],
        "example": 'controller.step(action="Teleport", position=dict(x=1,y=0.9,z=-1.5), rotation=dict(x=0,y=270,z=0), horizon=30, standing=True)',
        "preconditions": ["Hedef poz geçerli olmalı (duvar/çarpışma yok)."],
        "effects": ["Ajan pozu güncellenir."],
        "pddl_action": "teleport",
        "pddl_params": [("?a - agent"), ("?l - location"), ("?o - orientation")],
        "pddl_pre": ["(reachable-position ?l)", "(valid-pose ?a ?l ?o)"],
        "pddl_eff": ["(at-agent ?a ?l)", "(facing ?a ?o)"],
        "query": False,
    },
    "TeleportFull": {
        "category": "navigation",
        "source": "navigation.md",
        "description": "Teleport'un katı versiyonu; tüm serbestlik dereceleri zorunludur.",
        "params": [
            ("position", "dict", True, "-", "Global pozisyon (zorunlu)."),
            ("rotation", "dict", True, "-", "Gövde rotasyonu (zorunlu)."),
            ("horizon", "float", True, "-", "Kamera horizon (zorunlu)."),
            ("standing", "bool", True, "-", "Duruş durumu (zorunlu)."),
        ],
        "example": 'controller.step(action="TeleportFull", position=dict(x=1,y=0.9,z=-1.5), rotation=dict(x=0,y=270,z=0), horizon=30, standing=True)',
        "preconditions": ["Tüm parametreler geçerli olmalı."],
        "effects": ["Ajan pozu tam olarak ayarlanır."],
        "pddl_action": "teleport-full",
        "pddl_params": [("?a - agent"), ("?l - location"), ("?o - orientation"), ("?h - horizon")],
        "pddl_pre": ["(reachable-position ?l)", "(valid-full-pose ?a ?l ?o ?h)"],
        "pddl_eff": ["(at-agent ?a ?l)", "(facing ?a ?o)", "(camera-horizon ?a ?h)"],
        "query": False,
    },
    "GetReachablePositions": {
        "category": "query",
        "source": "metadata.md",
        "description": "Ajanın ulaşabileceği tüm grid pozisyonlarını BFS ile döndürür. Ortam durumunu değiştirmez.",
        "params": [],
        "example": 'positions = controller.step(action="GetReachablePositions").metadata["actionReturn"]',
        "preconditions": [],
        "effects": ["actionReturn: ulaşılabilir pozisyon listesi."],
        "pddl_action": "get-reachable-positions",
        "pddl_params": [("?a - agent")],
        "pddl_pre": [],
        "pddl_eff": [],
        "query": True,
    },
    "Done": {
        "category": "navigation",
        "source": "navigation.md",
        "description": "Görev tamamlandı sinyali verir. Ortam durumunu değiştirmez.",
        "params": [],
        "example": 'controller.step(action="Done")',
        "preconditions": [],
        "effects": ["Metadata temizlenmiş event döner."],
        "pddl_action": "done",
        "pddl_params": [("?a - agent")],
        "pddl_pre": ["(goal-achieved)"],
        "pddl_eff": ["(task-complete)"],
        "query": False,
    },
    # Interactive - Manipulation
    "PickupObject": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Belirtilen pickupable nesneyi ajanın eline alır.",
        "params": [
            ("objectId", "string", True, "-", "Hedef nesnenin objectId'si."),
            ("forceAction", "bool", False, "False", "visibilityDistance kısıtını yok sayar."),
            ("manualInteract", "bool", False, "False", "True ise nesne elde teleport olmaz."),
        ],
        "example": 'controller.step(action="PickupObject", objectId="Apple|1|1|1", forceAction=False, manualInteract=False)',
        "preconditions": ["Nesne pickupable=True.", "Ajan eli boş.", "Nesne görünür/erişilebilir.", "Çarpışma yok."],
        "effects": ["isPickedUp=True", "İçerdiği nesneler de birlikte alınabilir (receptacle)."],
        "pddl_action": "pickup-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(pickupable ?o)", "(hand-empty ?a)", "(visible ?o)", "(interactable ?a ?o)", "(not (holding ?a ?o))"],
        "pddl_eff": ["(holding ?a ?o)", "(not (hand-empty ?a))", "(not (on-surface ?o))"],
        "query": False,
    },
    "PutObject": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Tutulan nesneyi hedef receptacle üzerine/ içine yerleştirir.",
        "params": [
            ("objectId", "string", True, "-", "Hedef receptacle objectId."),
            ("forceAction", "bool", False, "False", "Receptacle kısıtlarını yok sayar."),
            ("placeStationary", "bool", False, "True", "True=deterministik yerleşim."),
        ],
        "example": 'controller.step(action="PutObject", objectId="CounterTop|1|1|1", forceAction=False, placeStationary=True)',
        "preconditions": ["Ajan nesne tutuyor.", "Hedef receptacle=True.", "Geçerli receptacle kısıtları."],
        "effects": ["Nesne receptacle'a yerleşir.", "isPickedUp=False"],
        "pddl_action": "put-object",
        "pddl_params": [("?a - agent"), ("?o - object"), ("?r - receptacle")],
        "pddl_pre": ["(holding ?a ?o)", "(receptacle ?r)", "(valid-receptacle-for ?o ?r)", "(visible ?r)"],
        "pddl_eff": ["(not (holding ?a ?o))", "(hand-empty ?a)", "(in-receptacle ?o ?r)", "(on-surface ?o)"],
        "query": False,
    },
    "DropHandObject": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Tutulan nesneyi bırakır; fizik motoru iniş noktasını belirler.",
        "params": [("forceAction", "bool", False, "False", "Çarpışma olsa bile bırakır.")],
        "example": 'controller.step(action="DropHandObject", forceAction=False)',
        "preconditions": ["Ajan nesne tutuyor.", "Çarpışma engeli yok (forceAction=False)."],
        "effects": ["Nesne serbest bırakılır.", "isPickedUp=False"],
        "pddl_action": "drop-object",
        "pddl_params": [("?a - agent"), ("?o - object"), ("?l - location")],
        "pddl_pre": ["(holding ?a ?o)", "(clear-drop ?a ?o)"],
        "pddl_eff": ["(not (holding ?a ?o))", "(hand-empty ?a)", "(at-object ?o ?l)", "(on-surface ?o)"],
        "query": False,
    },
    "ThrowObject": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Tutulan nesneyi ileri yönde belirtilen kuvvetle fırlatır.",
        "params": [
            ("moveMagnitude", "float", True, "-", "Fırlatma kuvveti (newton)."),
            ("forceAction", "bool", False, "False", "Çarpışma kısıtını yok sayar."),
        ],
        "example": 'controller.step(action="ThrowObject", moveMagnitude=150.0, forceAction=False)',
        "preconditions": ["Ajan nesne tutuyor."],
        "effects": ["Nesne fırlatılır.", "isPickedUp=False"],
        "pddl_action": "throw-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(holding ?a ?o)"],
        "pddl_eff": ["(not (holding ?a ?o))", "(hand-empty ?a)", "(in-motion ?o)", "(not (on-surface ?o))"],
        "query": False,
    },
    "MoveHeldObjectAhead": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Tutulan nesneyi ileri yönde hareket ettirir.",
        "params": [
            ("moveMagnitude", "float", True, "-", "Hareket mesafesi (metre)."),
            ("forceVisible", "bool", False, "False", "True ise nesne görünür kalmalı."),
        ],
        "example": 'controller.step(action="MoveHeldObjectAhead", moveMagnitude=0.1, forceVisible=False)',
        "preconditions": ["Ajan nesne tutuyor."],
        "effects": ["Tutulan nesne pozisyonu güncellenir."],
        "pddl_action": "move-held-ahead",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(holding ?a ?o)"],
        "pddl_eff": ["(held-offset ?a ?o ahead)"],
        "query": False,
    },
    "MoveHeldObjectBack": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Tutulan nesneyi geri yönde hareket ettirir.",
        "params": [("moveMagnitude", "float", True, "-", "Hareket mesafesi (metre)."), ("forceVisible", "bool", False, "False", "Görünürlük zorunluluğu.")],
        "example": 'controller.step("MoveHeldObjectBack")',
        "preconditions": ["Ajan nesne tutuyor."],
        "effects": ["Tutulan nesne pozisyonu güncellenir."],
        "pddl_action": "move-held-back",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(holding ?a ?o)"],
        "pddl_eff": ["(held-offset ?a ?o back)"],
        "query": False,
    },
    "MoveHeldObjectLeft": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Tutulan nesneyi sola hareket ettirir.",
        "params": [("moveMagnitude", "float", True, "-", "Hareket mesafesi (metre)."), ("forceVisible", "bool", False, "False", "Görünürlük zorunluluğu.")],
        "example": 'controller.step("MoveHeldObjectLeft")',
        "preconditions": ["Ajan nesne tutuyor."],
        "effects": ["Tutulan nesne pozisyonu güncellenir."],
        "pddl_action": "move-held-left",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(holding ?a ?o)"],
        "pddl_eff": ["(held-offset ?a ?o left)"],
        "query": False,
    },
    "MoveHeldObjectRight": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Tutulan nesneyi sağa hareket ettirir.",
        "params": [("moveMagnitude", "float", True, "-", "Hareket mesafesi (metre)."), ("forceVisible", "bool", False, "False", "Görünürlük zorunluluğu.")],
        "example": 'controller.step("MoveHeldObjectRight")',
        "preconditions": ["Ajan nesne tutuyor."],
        "effects": ["Tutulan nesne pozisyonu güncellenir."],
        "pddl_action": "move-held-right",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(holding ?a ?o)"],
        "pddl_eff": ["(held-offset ?a ?o right)"],
        "query": False,
    },
    "MoveHeldObjectUp": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Tutulan nesneyi yukarı hareket ettirir.",
        "params": [("moveMagnitude", "float", True, "-", "Hareket mesafesi (metre)."), ("forceVisible", "bool", False, "False", "Görünürlük zorunluluğu.")],
        "example": 'controller.step("MoveHeldObjectUp")',
        "preconditions": ["Ajan nesne tutuyor."],
        "effects": ["Tutulan nesne pozisyonu güncellenir."],
        "pddl_action": "move-held-up",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(holding ?a ?o)"],
        "pddl_eff": ["(held-offset ?a ?o up)"],
        "query": False,
    },
    "MoveHeldObjectDown": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Tutulan nesneyi aşağı hareket ettirir.",
        "params": [("moveMagnitude", "float", True, "-", "Hareket mesafesi (metre)."), ("forceVisible", "bool", False, "False", "Görünürlük zorunluluğu.")],
        "example": 'controller.step("MoveHeldObjectDown")',
        "preconditions": ["Ajan nesne tutuyor."],
        "effects": ["Tutulan nesne pozisyonu güncellenir."],
        "pddl_action": "move-held-down",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(holding ?a ?o)"],
        "pddl_eff": ["(held-offset ?a ?o down)"],
        "query": False,
    },
    "MoveHeldObject": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Tutulan nesneyi ahead/right/up eksenlerinde tek aksiyonla hareket ettirir.",
        "params": [
            ("ahead", "float", True, "-", "İleri mesafe (metre)."),
            ("right", "float", True, "-", "Sağ mesafe (metre)."),
            ("up", "float", True, "-", "Yukarı mesafe (metre)."),
            ("forceVisible", "bool", False, "False", "Görünürlük zorunluluğu."),
        ],
        "example": 'controller.step(action="MoveHeldObject", ahead=0.1, right=0.05, up=0.12, forceVisible=False)',
        "preconditions": ["Ajan nesne tutuyor."],
        "effects": ["Tutulan nesne pozisyonu güncellenir."],
        "pddl_action": "move-held-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(holding ?a ?o)"],
        "pddl_eff": ["(held-offset-combined ?a ?o)"],
        "query": False,
    },
    "RotateHeldObject": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Tutulan nesneyi pitch/yaw/roll veya sabit rotasyona ayarlar.",
        "params": [
            ("pitch", "float", False, "0", "Pitch artışı (derece)."),
            ("yaw", "float", False, "0", "Yaw artışı (derece)."),
            ("roll", "float", False, "0", "Roll artışı (derece)."),
            ("rotation", "dict", False, "None", "Sabit rotasyon {x,y,z} (alternatif)."),
        ],
        "example": 'controller.step(action="RotateHeldObject", pitch=90, yaw=25, roll=45)',
        "preconditions": ["Ajan nesne tutuyor."],
        "effects": ["Tutulan nesne rotasyonu güncellenir."],
        "pddl_action": "rotate-held-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(holding ?a ?o)"],
        "pddl_eff": ["(held-rotated ?a ?o)"],
        "query": False,
    },
    "DirectionalPush": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Nesneyi belirtilen açıda iter. pickupable veya moveable nesneler için.",
        "params": [
            ("objectId", "string", True, "-", "Hedef nesne."),
            ("moveMagnitude", "float", True, "-", "İtme kuvveti (newton)."),
            ("pushAngle", "float", True, "-", "İtme yönü [0:360], 0=ileri."),
            ("forceAction", "bool", False, "False", "Mesafe kısıtını yok sayar."),
        ],
        "example": 'controller.step(action="DirectionalPush", objectId="Sofa|3|2|1", moveMagnitude=100, pushAngle=90)',
        "preconditions": ["Nesne pickupable veya moveable.", "Görünür/erişilebilir."],
        "effects": ["Nesne hareket eder."],
        "pddl_action": "directional-push",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(moveable ?o)", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(in-motion ?o)"],
        "query": False,
    },
    "PushObject": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "DirectionalPush'un pushAngle=0 sözdizimsel kısayolu.",
        "params": [
            ("objectId", "string", True, "-", "Hedef nesne."),
            ("moveMagnitude", "float", True, "-", "İtme kuvveti."),
            ("forceAction", "bool", False, "False", "Mesafe kısıtını yok sayar."),
        ],
        "example": 'controller.step(action="PushObject", objectId="Mug|0.25|-0.27", forceAction=False)',
        "preconditions": ["Nesne pickupable veya moveable."],
        "effects": ["Nesne ileri itilir."],
        "pddl_action": "push-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(moveable ?o)", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(in-motion ?o)"],
        "query": False,
        "pddl_note": "PDDL'de directional-push(?o, 0) ile eşdeğer.",
    },
    "PullObject": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "DirectionalPush'un pushAngle=180 sözdizimsel kısayolu.",
        "params": [
            ("objectId", "string", True, "-", "Hedef nesne."),
            ("moveMagnitude", "float", True, "-", "Çekme kuvveti."),
            ("forceAction", "bool", False, "False", "Mesafe kısıtını yok sayar."),
        ],
        "example": 'controller.step(action="PullObject", objectId="Mug|0.25|-0.27", forceAction=False)',
        "preconditions": ["Nesne pickupable veya moveable."],
        "effects": ["Nesne geri çekilir."],
        "pddl_action": "pull-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(moveable ?o)", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(in-motion ?o)"],
        "query": False,
        "pddl_note": "PDDL'de directional-push(?o, 180) ile eşdeğer.",
    },
    "TouchThenApplyForce": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Ekran koordinatından ışın göndererek nesneye kuvvet uygular.",
        "params": [
            ("x", "float", True, "-", "Ekran x [0:1]."),
            ("y", "float", True, "-", "Ekran y [0:1]."),
            ("direction", "dict", True, "-", "İtme yön vektörü {x,y,z}."),
            ("moveMagnitude", "float", True, "-", "Kuvvet (newton)."),
            ("handDistance", "float", True, "-", "Maksimum el mesafesi (metre)."),
        ],
        "example": 'controller.step(action="TouchThenApplyForce", x=0.5, y=0.5, direction={"x":0,"y":1,"z":0}, moveMagnitude=80, handDistance=1.5)',
        "preconditions": ["Hedef görünür ve handDistance içinde.", "pickupable/moveable nesne."],
        "effects": ["Nesneye anlık kuvvet uygulanır.", "actionReturn geri bildirim döner."],
        "pddl_action": "touch-apply-force",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(visible ?o)", "(in-range ?a ?o)", "(moveable ?o)"],
        "pddl_eff": ["(in-motion ?o)"],
        "query": False,
    },
    "PlaceObjectAtPoint": {
        "category": "interactive",
        "source": "interactive.md",
        "description": "Nesneyi belirtilen global koordinata receptacle yüzeyine yerleştirir.",
        "params": [
            ("objectId", "string", True, "-", "Yerleştirilecek nesne."),
            ("position", "dict", True, "-", "Global (x,y,z) koordinat."),
        ],
        "example": 'controller.step(action="PlaceObjectAtPoint", objectId="Toaster|1|1|1", position={"x":-1.25,"y":1.0,"z":-1.0})',
        "preconditions": ["Nesne pickupable veya moveable.", "Geçerli yerleşim noktası."],
        "effects": ["Nesne belirtilen noktaya teleport edilir."],
        "pddl_action": "place-at-point",
        "pddl_params": [("?o - object"), ("?p - point")],
        "pddl_pre": ["(pickupable ?o)", "(valid-placement-point ?o ?p)"],
        "pddl_eff": ["(at-point ?o ?p)", "(on-surface ?o)"],
        "query": False,
    },
    "GetSpawnCoordinatesAboveReceptacle": {
        "category": "query",
        "source": "interactive.md",
        "description": "Receptacle üzerindeki geçerli spawn koordinatlarını döndürür.",
        "params": [
            ("objectId", "string", True, "-", "Hedef receptacle."),
            ("anywhere", "bool", False, "False", "Görüş dışı koordinatları da döndür."),
        ],
        "example": 'controller.step(action="GetSpawnCoordinatesAboveReceptacle", objectId="CounterTop|1|1|1", anywhere=False)',
        "preconditions": [],
        "effects": ["actionReturn: xyz koordinat listesi."],
        "pddl_action": "get-spawn-coordinates",
        "pddl_params": [("?r - receptacle")],
        "pddl_pre": ["(receptacle ?r)"],
        "pddl_eff": [],
        "query": True,
    },
    # Object State Changes
    "OpenObject": {
        "category": "object_state",
        "source": "object_state_changes.md",
        "description": "Açılabilir nesneyi belirtilen openness oranına açar.",
        "params": [
            ("objectId", "string", True, "-", "Hedef nesne."),
            ("openness", "float", False, "1", "Açıklık oranı [0:1]."),
            ("forceAction", "bool", False, "False", "Mesafe kısıtını yok sayar."),
        ],
        "example": 'controller.step(action="OpenObject", objectId="Book|0.25|-0.27|0.95", openness=1, forceAction=False)',
        "preconditions": ["openable=True.", "Görünür/erişilebilir.", "Çarpışma engeli yok."],
        "effects": ["openness güncellenir.", "isOpen=True (openness>0)."],
        "pddl_action": "open-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(openable ?o)", "(closed ?o)", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(not (closed ?o))", "(open ?o)"],
        "query": False,
    },
    "CloseObject": {
        "category": "object_state",
        "source": "object_state_changes.md",
        "description": "OpenObject'un openness=0 sözdizimsel kısayolu.",
        "params": [("objectId", "string", True, "-", "Hedef nesne."), ("forceAction", "bool", False, "False", "Mesafe kısıtını yok sayar.")],
        "example": 'controller.step(action="CloseObject", objectId="Book|0.25|-0.27|0.95", forceAction=False)',
        "preconditions": ["openable=True.", "Açık olmalı."],
        "effects": ["openness=0.", "isOpen=False"],
        "pddl_action": "close-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(openable ?o)", "(open ?o)", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(not (open ?o))", "(closed ?o)"],
        "query": False,
        "pddl_note": "PDDL'de open-object(?o, 0) ile eşdeğer.",
    },
    "BreakObject": {
        "category": "object_state",
        "source": "object_state_changes.md",
        "description": "Kırılabilir nesneyi kırar (geri alınamaz, reset gerekir).",
        "params": [("objectId", "string", True, "-", "Hedef nesne."), ("forceAction", "bool", False, "False", "Mesafe kısıtı.")],
        "example": 'controller.step(action="BreakObject", objectId="Vase|0.25|0.27|-0.95", forceAction=False)',
        "preconditions": ["breakable=True.", "Görünür/erişilebilir."],
        "effects": ["isBroken=True"],
        "pddl_action": "break-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(breakable ?o)", "(not (broken ?o))", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(broken ?o)", "(not (intact ?o))"],
        "query": False,
    },
    "CookObject": {
        "category": "object_state",
        "source": "object_state_changes.md",
        "description": "Pişirilebilir nesneyi pişirir (geri alınamaz).",
        "params": [("objectId", "string", True, "-", "Hedef nesne."), ("forceAction", "bool", False, "False", "Mesafe kısıtı.")],
        "example": 'controller.step(action="CookObject", objectId="Egg|0.25|-0.27|0.95", forceAction=False)',
        "preconditions": ["cookable=True.", "Görünür/erişilebilir."],
        "effects": ["isCooked=True"],
        "pddl_action": "cook-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(cookable ?o)", "(not (cooked ?o))", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(cooked ?o)", "(not (raw ?o))"],
        "query": False,
    },
    "SliceObject": {
        "category": "object_state",
        "source": "object_state_changes.md",
        "description": "Dilimlenebilir nesneyi dilimler; yeni dilim nesneleri oluşabilir.",
        "params": [("objectId", "string", True, "-", "Hedef nesne."), ("forceAction", "bool", False, "False", "Mesafe kısıtı.")],
        "example": 'controller.step(action="SliceObject", objectId="Potato|0.25|-0.27|0.95", forceAction=False)',
        "preconditions": ["sliceable=True.", "Görünür/erişilebilir."],
        "effects": ["isSliced=True", "Yeni dilim nesneleri oluşabilir."],
        "pddl_action": "slice-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(sliceable ?o)", "(not (sliced ?o))", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(sliced ?o)", "(not (whole ?o))"],
        "query": False,
    },
    "ToggleObjectOn": {
        "category": "object_state",
        "source": "object_state_changes.md",
        "description": "Toggleable nesneyi açık (on) durumuna getirir.",
        "params": [("objectId", "string", True, "-", "Hedef nesne."), ("forceAction", "bool", False, "False", "Mesafe kısıtı.")],
        "example": 'controller.step(action="ToggleObjectOn", objectId="LightSwitch|0.25|-0.27|0.95", forceAction=False)',
        "preconditions": ["toggleable=True.", "Kapalı olmalı.", "Görünür/erişilebilir."],
        "effects": ["isToggled=True"],
        "pddl_action": "toggle-on",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(toggleable ?o)", "(toggled-off ?o)", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(not (toggled-off ?o))", "(toggled-on ?o)"],
        "query": False,
    },
    "ToggleObjectOff": {
        "category": "object_state",
        "source": "object_state_changes.md",
        "description": "Toggleable nesneyi kapalı (off) durumuna getirir.",
        "params": [("objectId", "string", True, "-", "Hedef nesne."), ("forceAction", "bool", False, "False", "Mesafe kısıtı.")],
        "example": 'controller.step(action="ToggleObjectOff", objectId="LightSwitch|0.25|-0.27|0.95", forceAction=False)',
        "preconditions": ["toggleable=True.", "Açık olmalı."],
        "effects": ["isToggled=False"],
        "pddl_action": "toggle-off",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(toggleable ?o)", "(toggled-on ?o)", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(not (toggled-on ?o))", "(toggled-off ?o)"],
        "query": False,
    },
    "DirtyObject": {
        "category": "object_state",
        "source": "object_state_changes.md",
        "description": "Kirletilebilir nesneyi kirli yapar.",
        "params": [("objectId", "string", True, "-", "Hedef nesne."), ("forceAction", "bool", False, "False", "Mesafe kısıtı.")],
        "example": 'controller.step(action="DirtyObject", objectId="Mug|0.25|-0.27|0.95", forceAction=False)',
        "preconditions": ["dirtyable=True.", "Temiz olmalı."],
        "effects": ["isDirty=True"],
        "pddl_action": "dirty-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(dirtyable ?o)", "(clean ?o)", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(not (clean ?o))", "(dirty ?o)"],
        "query": False,
    },
    "CleanObject": {
        "category": "object_state",
        "source": "object_state_changes.md",
        "description": "Kirli nesneyi temizler.",
        "params": [("objectId", "string", True, "-", "Hedef nesne."), ("forceAction", "bool", False, "False", "Mesafe kısıtı.")],
        "example": 'controller.step(action="CleanObject", objectId="Mug|0.25|-0.27|0.95", forceAction=False)',
        "preconditions": ["dirtyable=True.", "Kirli olmalı."],
        "effects": ["isDirty=False"],
        "pddl_action": "clean-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(dirtyable ?o)", "(dirty ?o)", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(not (dirty ?o))", "(clean ?o)"],
        "query": False,
    },
    "FillObjectWithLiquid": {
        "category": "object_state",
        "source": "object_state_changes.md",
        "description": "Boş ve uyumlu nesneyi sıvı ile doldurur.",
        "params": [
            ("objectId", "string", True, "-", "Hedef nesne."),
            ("fillLiquid", "string", True, "-", "coffee, wine veya water."),
            ("forceAction", "bool", False, "False", "Mesafe kısıtı."),
        ],
        "example": 'controller.step(action="FillObjectWithLiquid", objectId="Mug|0.25|-0.27|0.95", fillLiquid="coffee", forceAction=False)',
        "preconditions": ["canFillWithLiquid=True.", "Boş olmalı.", "Görünür/erişilebilir."],
        "effects": ["isFilledWithLiquid=True", "fillLiquid ayarlanır."],
        "pddl_action": "fill-liquid",
        "pddl_params": [("?a - agent"), ("?o - object"), ("?l - liquid")],
        "pddl_pre": ["(can-fill ?o)", "(empty-liquid ?o)", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(not (empty-liquid ?o))", "(filled-with ?o ?l)"],
        "query": False,
    },
    "EmptyLiquidFromObject": {
        "category": "object_state",
        "source": "object_state_changes.md",
        "description": "Dolu nesnedeki sıvıyı boşaltır.",
        "params": [("objectId", "string", True, "-", "Hedef nesne."), ("forceAction", "bool", False, "False", "Mesafe kısıtı.")],
        "example": 'controller.step(action="EmptyLiquidFromObject", objectId="Mug|0.25|-0.27|0.95", forceAction=False)',
        "preconditions": ["isFilledWithLiquid=True."],
        "effects": ["isFilledWithLiquid=False", "fillLiquid=None"],
        "pddl_action": "empty-liquid",
        "pddl_params": [("?a - agent"), ("?o - object"), ("?l - liquid")],
        "pddl_pre": ["(filled-with ?o ?l)", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(not (filled-with ?o ?l))", "(empty-liquid ?o)"],
        "query": False,
    },
    "UseUpObject": {
        "category": "object_state",
        "source": "object_state_changes.md",
        "description": "Tüketilebilir nesnenin bir kısmını kullanır (tuvalet kağıdı vb.).",
        "params": [("objectId", "string", True, "-", "Hedef nesne."), ("forceAction", "bool", False, "False", "Mesafe kısıtı.")],
        "example": 'controller.step(action="UseUpObject", objectId="ToiletPaper|0.25|-0.27|0.95", forceAction=False)',
        "preconditions": ["canBeUsedUp=True.", "Tükenmemiş olmalı."],
        "effects": ["isUsedUp=True (veya kısmi tüketim)."],
        "pddl_action": "use-up-object",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(can-be-used-up ?o)", "(not (used-up ?o))", "(visible ?o)", "(interactable ?a ?o)"],
        "pddl_eff": ["(used-up ?o)"],
        "query": False,
    },
    # Set Object States
    "SetObjectPoses": {
        "category": "scene_setup",
        "source": "set_object_states.md",
        "description": "Sahnedeki nesnelerin pozisyon/rotasyonunu toplu ayarlar.",
        "params": [("objectPoses", "list[dict]", True, "-", "objectName, position, rotation listesi.")],
        "example": "controller.step(action='SetObjectPoses', objectPoses=[{...}])",
        "preconditions": ["Geçerli objectName ve koordinatlar."],
        "effects": ["Belirtilmeyen pickupable/moveable nesneler kaldırılır.", "Nesne pozları güncellenir."],
        "pddl_action": "set-object-poses",
        "pddl_params": [("?o - object"), ("?p - point"), ("?r - rotation")],
        "pddl_pre": [],
        "pddl_eff": ["(at-point ?o ?p)", "(object-rotation ?o ?r)"],
        "query": False,
    },
    "SetMassProperties": {
        "category": "scene_setup",
        "source": "set_object_states.md",
        "description": "Pickupable/moveable nesnenin kütle özelliklerini değiştirir.",
        "params": [
            ("objectId", "str", True, "-", "Hedef nesne."),
            ("mass", "float", True, "-", "Kütle (kg, >0)."),
            ("drag", "float", True, "-", "Sürüklenme katsayısı (>0)."),
            ("angularDrag", "float", True, "-", "Açısal sürüklenme (>0)."),
        ],
        "example": 'controller.step(action="SetMassProperties", objectId="Apple|+1.25|+0.25|-0.75", mass=22.5, drag=15.9, angularDrag=5.6)',
        "preconditions": ["Nesne moveable/pickupable."],
        "effects": ["Kütle özellikleri güncellenir."],
        "pddl_action": "set-mass-properties",
        "pddl_params": [("?o - object")],
        "pddl_pre": ["(moveable ?o)"],
        "pddl_eff": ["(mass-modified ?o)"],
        "query": False,
    },
    "SetRoomTempDecayTimeForType": {
        "category": "scene_setup",
        "source": "set_object_states.md",
        "description": "Belirli objectType için oda sıcaklığına dönüş süresini ayarlar.",
        "params": [
            ("objectType", "str", False, "None", "Nesne tipi."),
            ("TimeUntilRoomTemp", "float", True, "-", "Saniye cinsinden süre."),
        ],
        "example": 'controller.step(action="SetRoomTempDecayTimeForType", objectType="Bread", TimeUntilRoomTemp=20.0)',
        "preconditions": [],
        "effects": ["Tip bazlı sıcaklık decay süresi güncellenir."],
        "pddl_action": "set-temp-decay-type",
        "pddl_params": [("?t - objecttype")],
        "pddl_pre": [],
        "pddl_eff": ["(temp-decay-time ?t)"],
        "query": False,
    },
    "SetGlobalRoomTempDecayTime": {
        "category": "scene_setup",
        "source": "set_object_states.md",
        "description": "Tüm nesneler için global sıcaklık decay süresini ayarlar.",
        "params": [("TimeUntilRoomTemp", "float", True, "-", "Saniye cinsinden süre.")],
        "example": 'controller.step(action="SetGlobalRoomTempDecayTime", TimeUntilRoomTemp=20.0)',
        "preconditions": [],
        "effects": ["Global decay süresi güncellenir."],
        "pddl_action": "set-global-temp-decay",
        "pddl_params": [],
        "pddl_pre": [],
        "pddl_eff": ["(global-temp-decay-set)"],
        "query": False,
    },
    "SetDecayTemperatureBool": {
        "category": "scene_setup",
        "source": "set_object_states.md",
        "description": "Sıcaklık decay mekanizmasını açar/kapatır.",
        "params": [("allowDecayTemperature", "bool", False, "True", "Decay izni.")],
        "example": "controller.step(action='SetDecayTemperatureBool', allowDecayTemperature=False)",
        "preconditions": [],
        "effects": ["Sıcaklık decay davranışı değişir."],
        "pddl_action": "set-decay-temp-bool",
        "pddl_params": [],
        "pddl_pre": [],
        "pddl_eff": ["(temp-decay-enabled)"],
        "query": False,
    },
    "RemoveFromScene": {
        "category": "scene_setup",
        "source": "set_object_states.md",
        "description": "Nesneyi sahneden kalıcı olarak kaldırır.",
        "params": [("objectId", "str", True, "-", "Hedef nesne.")],
        "example": 'controller.step(action="RemoveFromScene", objectId="Mug|+0.25|-0.27|+1.05")',
        "preconditions": ["Nesne sahnede mevcut."],
        "effects": ["Nesne yok edilir (reset gerekir)."],
        "pddl_action": "remove-from-scene",
        "pddl_params": [("?o - object")],
        "pddl_pre": ["(exists ?o)"],
        "pddl_eff": ["(not (exists ?o))"],
        "query": False,
    },
    "DisableObject": {
        "category": "scene_setup",
        "source": "set_object_states.md",
        "description": "Nesneyi görünmez yapar (geçici, EnableObject ile geri alınabilir).",
        "params": [("objectId", "str", True, "-", "Hedef nesne.")],
        "example": 'controller.step(action="DisableObject", objectId="DiningTable|+1.0|+1.0|+1.0")',
        "preconditions": ["Nesne aktif."],
        "effects": ["Nesne devre dışı.", "Destekleyici nesne ise üstündekiler düşebilir."],
        "pddl_action": "disable-object",
        "pddl_params": [("?o - object")],
        "pddl_pre": ["(exists ?o)", "(enabled ?o)"],
        "pddl_eff": ["(not (enabled ?o))", "(disabled ?o)"],
        "query": False,
    },
    "EnableObject": {
        "category": "scene_setup",
        "source": "set_object_states.md",
        "description": "Devre dışı bırakılmış nesneyi tekrar aktif eder.",
        "params": [("objectId", "str", True, "-", "Hedef nesne.")],
        "example": 'controller.step(action="EnableObject", objectId="DiningTable|+1.0|+1.0|+1.0")',
        "preconditions": ["Nesne disabled durumda."],
        "effects": ["Nesne tekrar görünür.", "Orijinal konumuna döner."],
        "pddl_action": "enable-object",
        "pddl_params": [("?o - object")],
        "pddl_pre": ["(disabled ?o)"],
        "pddl_eff": ["(not (disabled ?o))", "(enabled ?o)"],
        "query": False,
    },
    # Physics
    "PausePhysicsAutoSim": {
        "category": "physics",
        "source": "initialization.md",
        "description": "Otomatik fizik simülasyonunu duraklatır.",
        "params": [],
        "example": 'controller.step("PausePhysicsAutoSim")',
        "preconditions": [],
        "effects": ["Auto-sim kapalı.", "AdvancePhysicsStep kullanılabilir."],
        "pddl_action": "pause-physics",
        "pddl_params": [],
        "pddl_pre": ["(physics-running)"],
        "pddl_eff": ["(not (physics-running))", "(physics-paused)"],
        "query": False,
    },
    "AdvancePhysicsStep": {
        "category": "physics",
        "source": "initialization.md",
        "description": "Fizik simülasyonunu belirtilen süre ilerletir.",
        "params": [("timeStep", "float", True, "-", "Simülasyon süresi (0, 0.05] saniye.")],
        "example": 'controller.step(action="AdvancePhysicsStep", timeStep=0.01)',
        "preconditions": ["PausePhysicsAutoSim çağrılmış olmalı."],
        "effects": ["Fizik durumu timeStep kadar ilerler."],
        "pddl_action": "advance-physics",
        "pddl_params": [],
        "pddl_pre": ["(physics-paused)"],
        "pddl_eff": ["(physics-advanced)"],
        "query": False,
    },
    "UnpausePhysicsAutoSim": {
        "category": "physics",
        "source": "initialization.md",
        "description": "Otomatik fizik simülasyonunu tekrar açar.",
        "params": [],
        "example": 'controller.step("UnpausePhysicsAutoSim")',
        "preconditions": ["Fizik duraklatılmış.", "Tüm nesneler durmuş olmalı (önerilir)."],
        "effects": ["Auto-sim açık."],
        "pddl_action": "unpause-physics",
        "pddl_params": [],
        "pddl_pre": ["(physics-paused)", "(scene-at-rest)"],
        "pddl_eff": ["(not (physics-paused))", "(physics-running)"],
        "query": False,
    },
    # Domain Randomization
    "RandomizeMaterials": {
        "category": "domain_randomization",
        "source": "domain.md",
        "description": "Sahnedeki tüm malzemeleri rastgele değiştirir.",
        "params": [
            ("useTrainMaterials", "Optional[bool]", False, "None", "Eğitim malzemeleri."),
            ("useValMaterials", "Optional[bool]", False, "None", "Validasyon malzemeleri."),
            ("useTestMaterials", "Optional[bool]", False, "None", "Test malzemeleri."),
            ("inRoomTypes", "List[str]", False, "None", "Oda tipleri filtresi."),
        ],
        "example": 'controller.step(action="RandomizeMaterials", useTrainMaterials=None, useValMaterials=None, useTestMaterials=None, inRoomTypes=None)',
        "preconditions": [],
        "effects": ["Malzemeler rastgelelenir.", "Reset ile eski haline döner."],
        "pddl_action": "randomize-materials",
        "pddl_params": [],
        "pddl_pre": [],
        "pddl_eff": ["(materials-randomized)"],
        "query": False,
    },
    "RandomizeLighting": {
        "category": "domain_randomization",
        "source": "domain.md",
        "description": "Sahne aydınlatmasını rastgele değiştirir.",
        "params": [
            ("brightness", "Tuple[float,float]", False, "(0.5, 1.5)", "Parlaklık aralığı."),
            ("randomizeColor", "bool", False, "True", "Renk rastgeleleme."),
            ("hue", "Tuple[float,float]", False, "(0, 1)", "Renk tonu aralığı."),
            ("saturation", "Tuple[float,float]", False, "(0.5, 1)", "Doygunluk aralığı."),
            ("synchronized", "bool", False, "False", "Tüm ışıklar senkron."),
        ],
        "example": 'controller.step(action="RandomizeLighting", brightness=(0.5, 1.5), randomizeColor=True, hue=(0, 1), saturation=(0.5, 1), synchronized=False)',
        "preconditions": [],
        "effects": ["Aydınlatma rastgelelenir."],
        "pddl_action": "randomize-lighting",
        "pddl_params": [],
        "pddl_pre": [],
        "pddl_eff": ["(lighting-randomized)"],
        "query": False,
    },
    "InitialRandomSpawn": {
        "category": "domain_randomization",
        "source": "domain.md",
        "description": "Pickupable nesnelerin pozisyonlarını rastgele yerleştirir.",
        "params": [
            ("randomSeed", "int", False, "0", "Rastgelelik tohumu."),
            ("forceVisible", "bool", False, "False", "Görünür alana zorla."),
            ("numPlacementAttempts", "int", False, "5", "Yerleştirme deneme sayısı."),
            ("placeStationary", "bool", False, "True", "Deterministik yerleşim."),
            ("numDuplicatesOfType", "list", False, "[]", "Tip bazlı kopya sayısı."),
            ("excludedReceptacles", "list", False, "[]", "Hariç tutulan receptacle'lar."),
            ("excludedObjectIds", "list", False, "[]", "Hariç tutulan nesneler."),
        ],
        "example": 'controller.step(action="InitialRandomSpawn", randomSeed=0, forceVisible=False)',
        "preconditions": ["Sahne reset edilmiş olmalı (seed doğruluğu için)."],
        "effects": ["Nesne pozisyonları değişir.", "objectId'ler yeniden hesaplanır."],
        "pddl_action": "initial-random-spawn",
        "pddl_params": [],
        "pddl_pre": [],
        "pddl_eff": ["(objects-randomized)"],
        "query": False,
    },
    "RandomizeColors": {
        "category": "domain_randomization",
        "source": "domain.md",
        "description": "Sahnedeki tüm nesnelerin renklerini rastgele değiştirir.",
        "params": [],
        "example": 'controller.step(action="RandomizeColors")',
        "preconditions": [],
        "effects": ["Nesne renkleri rastgelelenir."],
        "pddl_action": "randomize-colors",
        "pddl_params": [],
        "pddl_pre": [],
        "pddl_eff": ["(colors-randomized)"],
        "query": False,
    },
    # Query / Environment
    "GetObjectInFrame": {
        "category": "query",
        "source": "metadata.md",
        "description": "Ekran koordinatındaki nesnenin objectId'sini döndürür.",
        "params": [
            ("x", "float", True, "-", "Ekran x [0:1]."),
            ("y", "float", True, "-", "Ekran y [0:1]."),
            ("checkVisible", "bool", False, "False", "visibilityDistance kontrolü."),
        ],
        "example": 'query = controller.step(action="GetObjectInFrame", x=0.64, y=0.40, checkVisible=False)',
        "preconditions": [],
        "effects": ["actionReturn: objectId veya None."],
        "pddl_action": "get-object-in-frame",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": ["(in-frame ?o)"],
        "pddl_eff": [],
        "query": True,
    },
    "GetCoordinateFromRaycast": {
        "category": "query",
        "source": "metadata.md",
        "description": "Ekran koordinatından ışın göndererek çarpışma noktasının dünya koordinatını döndürür.",
        "params": [("x", "float", True, "-", "Ekran x [0:1]."), ("y", "float", True, "-", "Ekran y [0:1].")],
        "example": 'query = controller.step(action="GetCoordinateFromRaycast", x=0.64, y=0.40)',
        "preconditions": [],
        "effects": ["actionReturn: (x,y,z) koordinat."],
        "pddl_action": "get-coordinate-raycast",
        "pddl_params": [("?a - agent"), ("?p - point")],
        "pddl_pre": [],
        "pddl_eff": [],
        "query": True,
    },
    "GetInteractablePoses": {
        "category": "query",
        "source": "metadata.md",
        "description": "Bir nesneyle etkileşim kurulabilecek tüm ajan pozlarını döndürür.",
        "params": [
            ("objectId", "string", True, "-", "Hedef nesne."),
            ("positions", "list", False, "None", "Aranacak pozisyonlar."),
            ("rotations", "list", False, "None", "Aranacak rotasyonlar."),
            ("horizons", "list", False, "None", "Aranacak horizon değerleri."),
            ("standings", "list", False, "None", "Ayakta/çömelmiş durumları."),
        ],
        "example": 'event = controller.step(action="GetInteractablePoses", objectId="Apple|-1.0|+1.0|+1.5")',
        "preconditions": [],
        "effects": ["actionReturn: etkileşimli poz listesi."],
        "pddl_action": "get-interactable-poses",
        "pddl_params": [("?a - agent"), ("?o - object")],
        "pddl_pre": [],
        "pddl_eff": [],
        "query": True,
    },
    "AddThirdPartyCamera": {
        "category": "camera",
        "source": "metadata.md",
        "description": "Sahneye üçüncü parti kamera ekler.",
        "params": [
            ("position", "dict", True, "-", "Global pozisyon."),
            ("rotation", "dict", True, "-", "Global rotasyon."),
            ("fieldOfView", "int", False, "90", "Görüş alanı (derece)."),
        ],
        "example": 'event = controller.step(action="AddThirdPartyCamera", position=dict(x=-1.25,y=1,z=-1), rotation=dict(x=90,y=0,z=0), fieldOfView=90)',
        "preconditions": [],
        "effects": ["Yeni kamera eklenir.", "third_party_camera_frames erişilebilir."],
        "pddl_action": "add-third-party-camera",
        "pddl_params": [("?c - camera")],
        "pddl_pre": [],
        "pddl_eff": ["(camera-active ?c)"],
        "query": False,
    },
    "UpdateThirdPartyCamera": {
        "category": "camera",
        "source": "metadata.md",
        "description": "Mevcut üçüncü parti kameranın durumunu günceller.",
        "params": [
            ("thirdPartyCameraId", "int", True, "-", "Kamera indeksi."),
            ("position", "dict", False, "None", "Yeni pozisyon."),
            ("rotation", "dict", False, "None", "Yeni rotasyon."),
            ("fieldOfView", "int", False, "None", "Yeni FOV."),
        ],
        "example": 'controller.step(action="UpdateThirdPartyCamera", thirdPartyCameraId=0, position=dict(x=-1.25,y=1,z=-1))',
        "preconditions": ["Kamera mevcut olmalı."],
        "effects": ["Kamera parametreleri güncellenir."],
        "pddl_action": "update-third-party-camera",
        "pddl_params": [("?c - camera")],
        "pddl_pre": ["(camera-active ?c)"],
        "pddl_eff": ["(camera-updated ?c)"],
        "query": False,
    },
}

CATEGORY_LABELS = {
    "navigation": "Navigasyon",
    "interactive": "Etkileşim / Manipülasyon",
    "object_state": "Nesne Durumu Değişiklikleri",
    "scene_setup": "Sahne Kurulumu",
    "physics": "Fizik Simülasyonu",
    "domain_randomization": "Domain Randomizasyonu",
    "query": "Ortam Sorguları",
    "camera": "Kamera",
}


def format_params_table(params):
    if not params:
        return "_Parametre yok._\n"
    lines = ["| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |", "|-----------|-----|---------|------------|----------|"]
    for name, typ, required, default, desc in params:
        req = "Evet" if required else "Hayır"
        lines.append(f"| `{name}` | {typ} | {req} | {default} | {desc} |")
    return "\n".join(lines) + "\n"


def format_list(items):
    if not items:
        return "_Yok._\n"
    return "\n".join(f"- {item}" for item in items) + "\n"


def generate_api_doc(name, data):
    cat = CATEGORY_LABELS.get(data["category"], data["category"])
    query_note = "\n> **Not:** Bu bir sorgu aksiyonudur; ortam durumunu değiştirmez.\n" if data.get("query") else ""
    return f"""# {name}

**Kategori:** {cat}  
**Kaynak:** `raw/{data['source']}`  
**Sorgu Aksiyonu:** {'Evet' if data.get('query') else 'Hayır'}

## Açıklama

{data['description']}
{query_note}
## Kullanım

```python
{data['example']}
```

## Parametreler

{format_params_table(data['params'])}
## Ön Koşullar

{format_list(data['preconditions'])}
## Etkiler

{format_list(data['effects'])}

## İlgili PDDL Eşlemesi

→ [`pddl_mappings/{name}.md`](../pddl_mappings/{name}.md)
"""


def generate_pddl_doc(name, data):
    params_str = " ".join(data["pddl_params"])
    pre_str = "\n    ".join(data["pddl_pre"]) if data["pddl_pre"] else ""
    eff_str = "\n    ".join(data["pddl_eff"]) if data["pddl_eff"] else ""
    note = data.get("pddl_note", "")
    note_section = f"\n## Notlar\n\n{note}\n" if note else ""
    query_section = "\n> **Sorgu aksiyonu:** PDDL'de durum değiştirmez; `actionReturn` sembolik olarak `known(?result)` üretir.\n" if data.get("query") else ""

    pre_block = f":precondition (and\n    {pre_str})" if pre_str else ""
    eff_block = f":effect (and\n    {eff_str})" if eff_str else ""

    if data.get("query"):
        eff_block = ":effect (and\n    (increase (total-cost) 0))"

    return f"""# {name} → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `{name}`  
**PDDL Aksiyonu:** `{data['pddl_action']}`  
**Kategori:** {CATEGORY_LABELS.get(data['category'], data['category'])}
{query_section}
## PDDL Tanımı

```pddl
(:action {data['pddl_action']}
  :parameters ({params_str})
  {pre_block}
  {eff_block}
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

{format_list(data['preconditions'])}
## AI2-THOR Etkileri → PDDL Etkileri

{format_list(data['effects'])}

## PDDL Ön Koşulları

{format_list(data['pddl_pre']) if data['pddl_pre'] else '_Ön koşul yok (sorgu veya kurulum aksiyonu)._'}

## PDDL Etkileri

{format_list(data['pddl_eff']) if data['pddl_eff'] else '_Durum değişikliği yok._'}
{note_section}
## İlgili API Dokümantasyonu

→ [`ai2thor_api/{name}.md`](../ai2thor_api/{name}.md)
"""


def generate_domain_md():
  predicates = [
    ("at-agent", "?a - agent ?l - location", "Ajanın konumu"),
    ("facing", "?a - agent ?o - orientation", "Ajanın baktığı yön"),
    ("camera-horizon", "?a - agent ?h - horizon", "Kamera pitch açısı"),
    ("standing", "?a - agent", "Ajan ayakta"),
    ("crouching", "?a - agent", "Ajan çömelmiş"),
    ("hand-empty", "?a - agent", "Ajan eli boş"),
    ("holding", "?a - agent ?o - object", "Ajan nesne tutuyor"),
    ("visible", "?o - object", "Nesne görünür"),
    ("interactable", "?a - agent ?o - object", "Nesne ile etkileşilebilir"),
    ("pickupable", "?o - object", "Nesne alınabilir"),
    ("moveable", "?o - object", "Nesne itilebilir"),
    ("receptacle", "?r - receptacle", "Receptacle nesne"),
    ("in-receptacle", "?o - object ?r - receptacle", "Nesne receptacle içinde"),
    ("on-surface", "?o - object", "Nesne yüzeyde"),
    ("openable", "?o - object", "Açılabilir"),
    ("open", "?o - object", "Açık"),
    ("closed", "?o - object", "Kapalı"),
    ("breakable", "?o - object", "Kırılabilir"),
    ("broken", "?o - object", "Kırık"),
    ("cookable", "?o - object", "Pişirilebilir"),
    ("cooked", "?o - object", "Pişmiş"),
    ("sliceable", "?o - object", "Dilimlenebilir"),
    ("sliced", "?o - object", "Dilimlenmiş"),
    ("toggleable", "?o - object", "Açılıp kapatılabilir"),
    ("toggled-on", "?o - object", "Açık (on)"),
    ("toggled-off", "?o - object", "Kapalı (off)"),
    ("dirtyable", "?o - object", "Kirletilebilir"),
    ("dirty", "?o - object", "Kirli"),
    ("clean", "?o - object", "Temiz"),
    ("can-fill", "?o - object", "Sıvı ile doldurulabilir"),
    ("filled-with", "?o - object ?l - liquid", "Sıvı ile dolu"),
    ("empty-liquid", "?o - object", "Sıvısız"),
    ("can-be-used-up", "?o - object", "Tüketilebilir"),
    ("used-up", "?o - object", "Tükenmiş"),
    ("exists", "?o - object", "Nesne sahnede mevcut"),
    ("enabled", "?o - object", "Nesne aktif"),
    ("disabled", "?o - object", "Nesne devre dışı"),
    ("in-motion", "?o - object", "Nesne hareket halinde"),
    ("physics-running", "", "Fizik simülasyonu aktif"),
    ("physics-paused", "", "Fizik duraklatılmış"),
    ("scene-at-rest", "", "Sahne durgun"),
    ("reachable-position", "?l - location", "Ulaşılabilir pozisyon"),
    ("goal-achieved", "", "Hedef durum sağlandı"),
    ("task-complete", "", "Görev tamamlandı"),
  ]

  def format_predicate(name, sig):
      if not sig:
          return f"  ({name})"
      vars_only = " ".join(re.findall(r"\?\w+", sig))
      return f"  ({name} {vars_only})"

  pred_lines = "\n".join(format_predicate(p[0], p[1]) for p in predicates)
  types = """  agent - object
  object
  receptacle - object
  location
  orientation
  horizon
  liquid
  point
  rotation
  objecttype
  camera"""

  action_names = [data["pddl_action"] for data in ACTIONS.values()]

  return f"""# AI2-THOR PDDL Domain

Bu dosya, AI2-THOR aksiyonlarının sembolik planlama için kullanılan PDDL domain tanımını özetler.

**Oluşturulma:** {date.today().isoformat()}  
**Toplam Aksiyon:** {len(ACTIONS)}

## Tipler

```pddl
(:types
{types}
)
```

## Predikatlar

```pddl
(:predicates
{pred_lines}
)
```

## Aksiyonlar

Toplam **{len(action_names)}** aksiyon tanımlıdır. Her aksiyonun detaylı eşlemesi `pddl_mappings/` altındaki ilgili dosyada bulunur.

| Kategori | Aksiyonlar |
|----------|------------|
"""


def generate_index():
    by_cat = {}
    for name, data in sorted(ACTIONS.items()):
        by_cat.setdefault(data["category"], []).append(name)

    lines = [
        "# Wiki İndeksi — AI2-THOR Neuro-Symbolic Bilgi Tabanı",
        "",
        f"**Son güncelleme:** {date.today().isoformat()}",
        "",
        "Bu wiki, `/raw/` klasöründeki AI2-THOR dokümantasyonundan türetilmiştir.",
        "",
        "## Yapı",
        "",
        "| Klasör | Açıklama |",
        "|--------|----------|",
        "| [`ai2thor_api/`](ai2thor_api/) | Her AI2-THOR aksiyonu için API referansı |",
        "| [`pddl_mappings/`](pddl_mappings/) | AI2-THOR → PDDL eşlemeleri |",
        "| [`pddl_mappings/domain.md`](pddl_mappings/domain.md) | PDDL domain özeti |",
        "",
        f"**Toplam aksiyon sayısı:** {len(ACTIONS)}",
        "",
        "## Aksiyonlar (Kategoriye Göre)",
        "",
    ]

    for cat, names in sorted(by_cat.items()):
        label = CATEGORY_LABELS.get(cat, cat)
        lines.append(f"### {label}")
        lines.append("")
        for n in sorted(names):
            lines.append(f"- [`{n}`](ai2thor_api/{n}.md) · [PDDL](pddl_mappings/{n}.md)")
        lines.append("")

    lines.extend([
        "## Temel Kavramlar",
        "",
        "Kaynak: `raw/concepts.md`",
        "",
        "- **Agent:** Sahne içinde gezinen ve nesnelerle etkileşen kapsül şeklinde varlık",
        "- **Scene:** Mutfak, Oturma Odası, Yatak Odası, Banyo (her biri 30 sahne)",
        "- **Action:** Ajanın gerçekleştirdiği ayrık komut (ör. MoveAhead, PickupObject)",
        "- **Sim Object:** Etkileşilebilir nesne; ObjectType'a göre özellikler taşır",
        "- **Visibility:** Nesne karede görünür + visibilityDistance içinde + engelsiz",
        "- **Interactability:** Görünür VE engelsiz (visible ⊄ interactable)",
        "- **Receptacle:** Başka nesneleri barındırabilen nesne (TableTop, Bowl, vb.)",
        "",
        "## Kullanım Notları",
        "",
        "1. AI2-THOR kodu yazarken `pddl_mappings/` altındaki ön koşullara uyulmalıdır.",
        "2. `forceAction=True` PDDL'de `(force ?a)` veya mesafe kısıtı bypass semantiği ile modellenir.",
        "3. Sorgu aksiyonları (`GetReachablePositions`, vb.) durum değiştirmez.",
        "4. Sözdizimsel kısayollar: `CloseObject`→`OpenObject(0)`, `PushObject`→`DirectionalPush(0)`, `PullObject`→`DirectionalPush(180)`.",
        "",
    ])
    return "\n".join(lines)


def generate_log():
    return f"""# Wiki Değişiklik Günlüğü

## {date.today().isoformat()} — İlk Oluşturma

### Yapılan İşlemler

1. `/raw/` klasöründeki 11 markdown dosyası incelendi.
2. AI2-THOR `controller.step()` aksiyonları filtrelendi.
3. **{len(ACTIONS)}** aksiyon için `/wiki/ai2thor_api/` altında ayrı `.md` dosyaları oluşturuldu.
4. Her aksiyon için `/wiki/pddl_mappings/` altında PDDL eşleme dosyaları tasarlandı.
5. `/wiki/pddl_mappings/domain.md` PDDL domain özeti eklendi.
6. `/wiki/index.md` ve `/wiki/log.md` oluşturuldu.

### Kaynak Dosyalar

| Raw Dosya | İçerik |
|-----------|--------|
| `navigation.md` | Navigasyon aksiyonları |
| `interactive.md` | Manipülasyon ve fizik etkileşimleri |
| `object_state_changes.md` | Nesne durumu değişiklikleri |
| `set_object_states.md` | Sahne kurulum aksiyonları |
| `initialization.md` | Fizik simülasyon kontrolü |
| `domain.md` | Domain randomizasyonu |
| `metadata.md` | Ortam sorguları ve kamera |
| `concepts.md` | Temel kavramlar (aksiyon değil) |
| `installation.md` | Kurulum (aksiyon değil) |
| `scenes.md` | Sahne listesi (aksiyon değil) |
| `object_types.md` | Nesne tipleri (aksiyon değil) |

### Kategori Dağılımı

"""


def main():
    WIKI_API.mkdir(parents=True, exist_ok=True)
    WIKI_PDDL.mkdir(parents=True, exist_ok=True)

    for name, data in ACTIONS.items():
        (WIKI_API / f"{name}.md").write_text(generate_api_doc(name, data), encoding="utf-8")
        (WIKI_PDDL / f"{name}.md").write_text(generate_pddl_doc(name, data), encoding="utf-8")

    domain_content = generate_domain_md()
    by_cat = {}
    for name, data in ACTIONS.items():
        by_cat.setdefault(data["category"], []).append(f"`{data['pddl_action']}`")
    table_rows = []
    for cat in sorted(by_cat):
        label = CATEGORY_LABELS.get(cat, cat)
        table_rows.append(f"| {label} | {', '.join(sorted(by_cat[cat]))} |")
    domain_content += "\n".join(table_rows) + "\n"
    (WIKI_PDDL / "domain.md").write_text(domain_content, encoding="utf-8")

    log_content = generate_log()
    cat_counts = {}
    for data in ACTIONS.values():
        cat_counts[data["category"]] = cat_counts.get(data["category"], 0) + 1
    for cat, count in sorted(cat_counts.items()):
        log_content += f"- **{CATEGORY_LABELS.get(cat, cat)}:** {count} aksiyon\n"
    log_content += f"\n### Üretim\n\n- Betik: `scripts/generate_wiki.py`\n- Toplam dosya: {len(ACTIONS) * 2 + 2} (API + PDDL + index + domain)\n"

    (ROOT / "wiki" / "index.md").write_text(generate_index(), encoding="utf-8")
    (ROOT / "wiki" / "log.md").write_text(log_content, encoding="utf-8")

    print(f"Generated {len(ACTIONS)} API docs, {len(ACTIONS)} PDDL mappings, index, domain, log")


if __name__ == "__main__":
    main()
