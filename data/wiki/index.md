# Wiki İndeksi — AI2-THOR Neuro-Symbolic Bilgi Tabanı

**Son güncelleme:** 2026-06-22

Bu wiki, `/raw/` klasöründeki AI2-THOR dokümantasyonundan türetilmiştir.

## Yapı

| Klasör | Açıklama |
|--------|----------|
| [`ai2thor_api/`](ai2thor_api/) | Her AI2-THOR aksiyonu için API referansı |
| [`pddl_mappings/`](pddl_mappings/) | AI2-THOR → PDDL eşlemeleri |
| [`pddl_mappings/domain.md`](pddl_mappings/domain.md) | PDDL domain özeti |

**Toplam aksiyon sayısı:** 64

## Aksiyonlar (Kategoriye Göre)

### Kamera

- [`AddThirdPartyCamera`](ai2thor_api/AddThirdPartyCamera.md) · [PDDL](pddl_mappings/AddThirdPartyCamera.md)
- [`UpdateThirdPartyCamera`](ai2thor_api/UpdateThirdPartyCamera.md) · [PDDL](pddl_mappings/UpdateThirdPartyCamera.md)

### Domain Randomizasyonu

- [`InitialRandomSpawn`](ai2thor_api/InitialRandomSpawn.md) · [PDDL](pddl_mappings/InitialRandomSpawn.md)
- [`RandomizeColors`](ai2thor_api/RandomizeColors.md) · [PDDL](pddl_mappings/RandomizeColors.md)
- [`RandomizeLighting`](ai2thor_api/RandomizeLighting.md) · [PDDL](pddl_mappings/RandomizeLighting.md)
- [`RandomizeMaterials`](ai2thor_api/RandomizeMaterials.md) · [PDDL](pddl_mappings/RandomizeMaterials.md)

### Etkileşim / Manipülasyon

- [`DirectionalPush`](ai2thor_api/DirectionalPush.md) · [PDDL](pddl_mappings/DirectionalPush.md)
- [`DropHandObject`](ai2thor_api/DropHandObject.md) · [PDDL](pddl_mappings/DropHandObject.md)
- [`MoveHeldObject`](ai2thor_api/MoveHeldObject.md) · [PDDL](pddl_mappings/MoveHeldObject.md)
- [`MoveHeldObjectAhead`](ai2thor_api/MoveHeldObjectAhead.md) · [PDDL](pddl_mappings/MoveHeldObjectAhead.md)
- [`MoveHeldObjectBack`](ai2thor_api/MoveHeldObjectBack.md) · [PDDL](pddl_mappings/MoveHeldObjectBack.md)
- [`MoveHeldObjectDown`](ai2thor_api/MoveHeldObjectDown.md) · [PDDL](pddl_mappings/MoveHeldObjectDown.md)
- [`MoveHeldObjectLeft`](ai2thor_api/MoveHeldObjectLeft.md) · [PDDL](pddl_mappings/MoveHeldObjectLeft.md)
- [`MoveHeldObjectRight`](ai2thor_api/MoveHeldObjectRight.md) · [PDDL](pddl_mappings/MoveHeldObjectRight.md)
- [`MoveHeldObjectUp`](ai2thor_api/MoveHeldObjectUp.md) · [PDDL](pddl_mappings/MoveHeldObjectUp.md)
- [`PickupObject`](ai2thor_api/PickupObject.md) · [PDDL](pddl_mappings/PickupObject.md)
- [`PlaceObjectAtPoint`](ai2thor_api/PlaceObjectAtPoint.md) · [PDDL](pddl_mappings/PlaceObjectAtPoint.md)
- [`PullObject`](ai2thor_api/PullObject.md) · [PDDL](pddl_mappings/PullObject.md)
- [`PushObject`](ai2thor_api/PushObject.md) · [PDDL](pddl_mappings/PushObject.md)
- [`PutObject`](ai2thor_api/PutObject.md) · [PDDL](pddl_mappings/PutObject.md)
- [`RotateHeldObject`](ai2thor_api/RotateHeldObject.md) · [PDDL](pddl_mappings/RotateHeldObject.md)
- [`ThrowObject`](ai2thor_api/ThrowObject.md) · [PDDL](pddl_mappings/ThrowObject.md)
- [`TouchThenApplyForce`](ai2thor_api/TouchThenApplyForce.md) · [PDDL](pddl_mappings/TouchThenApplyForce.md)

### Navigasyon

- [`Crouch`](ai2thor_api/Crouch.md) · [PDDL](pddl_mappings/Crouch.md)
- [`Done`](ai2thor_api/Done.md) · [PDDL](pddl_mappings/Done.md)
- [`LookDown`](ai2thor_api/LookDown.md) · [PDDL](pddl_mappings/LookDown.md)
- [`LookUp`](ai2thor_api/LookUp.md) · [PDDL](pddl_mappings/LookUp.md)
- [`MoveAhead`](ai2thor_api/MoveAhead.md) · [PDDL](pddl_mappings/MoveAhead.md)
- [`MoveBack`](ai2thor_api/MoveBack.md) · [PDDL](pddl_mappings/MoveBack.md)
- [`MoveLeft`](ai2thor_api/MoveLeft.md) · [PDDL](pddl_mappings/MoveLeft.md)
- [`MoveRight`](ai2thor_api/MoveRight.md) · [PDDL](pddl_mappings/MoveRight.md)
- [`RotateLeft`](ai2thor_api/RotateLeft.md) · [PDDL](pddl_mappings/RotateLeft.md)
- [`RotateRight`](ai2thor_api/RotateRight.md) · [PDDL](pddl_mappings/RotateRight.md)
- [`Stand`](ai2thor_api/Stand.md) · [PDDL](pddl_mappings/Stand.md)
- [`Teleport`](ai2thor_api/Teleport.md) · [PDDL](pddl_mappings/Teleport.md)
- [`TeleportFull`](ai2thor_api/TeleportFull.md) · [PDDL](pddl_mappings/TeleportFull.md)

### Nesne Durumu Değişiklikleri

- [`BreakObject`](ai2thor_api/BreakObject.md) · [PDDL](pddl_mappings/BreakObject.md)
- [`CleanObject`](ai2thor_api/CleanObject.md) · [PDDL](pddl_mappings/CleanObject.md)
- [`CloseObject`](ai2thor_api/CloseObject.md) · [PDDL](pddl_mappings/CloseObject.md)
- [`CookObject`](ai2thor_api/CookObject.md) · [PDDL](pddl_mappings/CookObject.md)
- [`DirtyObject`](ai2thor_api/DirtyObject.md) · [PDDL](pddl_mappings/DirtyObject.md)
- [`EmptyLiquidFromObject`](ai2thor_api/EmptyLiquidFromObject.md) · [PDDL](pddl_mappings/EmptyLiquidFromObject.md)
- [`FillObjectWithLiquid`](ai2thor_api/FillObjectWithLiquid.md) · [PDDL](pddl_mappings/FillObjectWithLiquid.md)
- [`OpenObject`](ai2thor_api/OpenObject.md) · [PDDL](pddl_mappings/OpenObject.md)
- [`SliceObject`](ai2thor_api/SliceObject.md) · [PDDL](pddl_mappings/SliceObject.md)
- [`ToggleObjectOff`](ai2thor_api/ToggleObjectOff.md) · [PDDL](pddl_mappings/ToggleObjectOff.md)
- [`ToggleObjectOn`](ai2thor_api/ToggleObjectOn.md) · [PDDL](pddl_mappings/ToggleObjectOn.md)
- [`UseUpObject`](ai2thor_api/UseUpObject.md) · [PDDL](pddl_mappings/UseUpObject.md)

### Fizik Simülasyonu

- [`AdvancePhysicsStep`](ai2thor_api/AdvancePhysicsStep.md) · [PDDL](pddl_mappings/AdvancePhysicsStep.md)
- [`PausePhysicsAutoSim`](ai2thor_api/PausePhysicsAutoSim.md) · [PDDL](pddl_mappings/PausePhysicsAutoSim.md)
- [`UnpausePhysicsAutoSim`](ai2thor_api/UnpausePhysicsAutoSim.md) · [PDDL](pddl_mappings/UnpausePhysicsAutoSim.md)

### Ortam Sorguları

- [`GetCoordinateFromRaycast`](ai2thor_api/GetCoordinateFromRaycast.md) · [PDDL](pddl_mappings/GetCoordinateFromRaycast.md)
- [`GetInteractablePoses`](ai2thor_api/GetInteractablePoses.md) · [PDDL](pddl_mappings/GetInteractablePoses.md)
- [`GetObjectInFrame`](ai2thor_api/GetObjectInFrame.md) · [PDDL](pddl_mappings/GetObjectInFrame.md)
- [`GetReachablePositions`](ai2thor_api/GetReachablePositions.md) · [PDDL](pddl_mappings/GetReachablePositions.md)
- [`GetSpawnCoordinatesAboveReceptacle`](ai2thor_api/GetSpawnCoordinatesAboveReceptacle.md) · [PDDL](pddl_mappings/GetSpawnCoordinatesAboveReceptacle.md)

### Sahne Kurulumu

- [`DisableObject`](ai2thor_api/DisableObject.md) · [PDDL](pddl_mappings/DisableObject.md)
- [`EnableObject`](ai2thor_api/EnableObject.md) · [PDDL](pddl_mappings/EnableObject.md)
- [`RemoveFromScene`](ai2thor_api/RemoveFromScene.md) · [PDDL](pddl_mappings/RemoveFromScene.md)
- [`SetDecayTemperatureBool`](ai2thor_api/SetDecayTemperatureBool.md) · [PDDL](pddl_mappings/SetDecayTemperatureBool.md)
- [`SetGlobalRoomTempDecayTime`](ai2thor_api/SetGlobalRoomTempDecayTime.md) · [PDDL](pddl_mappings/SetGlobalRoomTempDecayTime.md)
- [`SetMassProperties`](ai2thor_api/SetMassProperties.md) · [PDDL](pddl_mappings/SetMassProperties.md)
- [`SetObjectPoses`](ai2thor_api/SetObjectPoses.md) · [PDDL](pddl_mappings/SetObjectPoses.md)
- [`SetRoomTempDecayTimeForType`](ai2thor_api/SetRoomTempDecayTimeForType.md) · [PDDL](pddl_mappings/SetRoomTempDecayTimeForType.md)

## Temel Kavramlar

Kaynak: `raw/concepts.md`

- **Agent:** Sahne içinde gezinen ve nesnelerle etkileşen kapsül şeklinde varlık
- **Scene:** Mutfak, Oturma Odası, Yatak Odası, Banyo (her biri 30 sahne)
- **Action:** Ajanın gerçekleştirdiği ayrık komut (ör. MoveAhead, PickupObject)
- **Sim Object:** Etkileşilebilir nesne; ObjectType'a göre özellikler taşır
- **Visibility:** Nesne karede görünür + visibilityDistance içinde + engelsiz
- **Interactability:** Görünür VE engelsiz (visible ⊄ interactable)
- **Receptacle:** Başka nesneleri barındırabilen nesne (TableTop, Bowl, vb.)

## Kullanım Notları

1. AI2-THOR kodu yazarken `pddl_mappings/` altındaki ön koşullara uyulmalıdır.
2. `forceAction=True` PDDL'de `(force ?a)` veya mesafe kısıtı bypass semantiği ile modellenir.
3. Sorgu aksiyonları (`GetReachablePositions`, vb.) durum değiştirmez.
4. Sözdizimsel kısayollar: `CloseObject`→`OpenObject(0)`, `PushObject`→`DirectionalPush(0)`, `PullObject`→`DirectionalPush(180)`.
