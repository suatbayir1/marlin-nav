# AI2-THOR PDDL Domain

Bu dosya, AI2-THOR aksiyonlarının sembolik planlama için kullanılan PDDL domain tanımını özetler.

**Oluşturulma:** 2026-06-22  
**Toplam Aksiyon:** 64

## Tipler

```pddl
(:types
  agent - object
  object
  receptacle - object
  location
  orientation
  horizon
  liquid
  point
  rotation
  objecttype
  camera
)
```

## Predikatlar

```pddl
(:predicates
  (at-agent ?a ?l)
  (facing ?a ?o)
  (camera-horizon ?a ?h)
  (standing ?a)
  (crouching ?a)
  (hand-empty ?a)
  (holding ?a ?o)
  (visible ?o)
  (interactable ?a ?o)
  (pickupable ?o)
  (moveable ?o)
  (receptacle ?r)
  (in-receptacle ?o ?r)
  (on-surface ?o)
  (openable ?o)
  (open ?o)
  (closed ?o)
  (breakable ?o)
  (broken ?o)
  (cookable ?o)
  (cooked ?o)
  (sliceable ?o)
  (sliced ?o)
  (toggleable ?o)
  (toggled-on ?o)
  (toggled-off ?o)
  (dirtyable ?o)
  (dirty ?o)
  (clean ?o)
  (can-fill ?o)
  (filled-with ?o ?l)
  (empty-liquid ?o)
  (can-be-used-up ?o)
  (used-up ?o)
  (exists ?o)
  (enabled ?o)
  (disabled ?o)
  (in-motion ?o)
  (physics-running)
  (physics-paused)
  (scene-at-rest)
  (reachable-position ?l)
  (goal-achieved)
  (task-complete)
)
```

## Aksiyonlar

Toplam **64** aksiyon tanımlıdır. Her aksiyonun detaylı eşlemesi `pddl_mappings/` altındaki ilgili dosyada bulunur.

| Kategori | Aksiyonlar |
|----------|------------|
| Kamera | `add-third-party-camera`, `update-third-party-camera` |
| Domain Randomizasyonu | `initial-random-spawn`, `randomize-colors`, `randomize-lighting`, `randomize-materials` |
| Etkileşim / Manipülasyon | `directional-push`, `drop-object`, `move-held-ahead`, `move-held-back`, `move-held-down`, `move-held-left`, `move-held-object`, `move-held-right`, `move-held-up`, `pickup-object`, `place-at-point`, `pull-object`, `push-object`, `put-object`, `rotate-held-object`, `throw-object`, `touch-apply-force` |
| Navigasyon | `crouch`, `done`, `look-down`, `look-up`, `move-ahead`, `move-back`, `move-left`, `move-right`, `rotate-left`, `rotate-right`, `stand`, `teleport-full`, `teleport` |
| Nesne Durumu Değişiklikleri | `break-object`, `clean-object`, `close-object`, `cook-object`, `dirty-object`, `empty-liquid`, `fill-liquid`, `open-object`, `slice-object`, `toggle-off`, `toggle-on`, `use-up-object` |
| Fizik Simülasyonu | `advance-physics`, `pause-physics`, `unpause-physics` |
| Ortam Sorguları | `get-coordinate-raycast`, `get-interactable-poses`, `get-object-in-frame`, `get-reachable-positions`, `get-spawn-coordinates` |
| Sahne Kurulumu | `disable-object`, `enable-object`, `remove-from-scene`, `set-decay-temp-bool`, `set-global-temp-decay`, `set-mass-properties`, `set-object-poses`, `set-temp-decay-type` |
