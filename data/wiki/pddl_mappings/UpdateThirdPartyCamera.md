# UpdateThirdPartyCamera → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `UpdateThirdPartyCamera`  
**PDDL Aksiyonu:** `update-third-party-camera`  
**Kategori:** Kamera

## PDDL Tanımı

```pddl
(:action update-third-party-camera
  :parameters (?c - camera)
  :precondition (and
    (camera-active ?c))
  :effect (and
    (camera-updated ?c))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Kamera mevcut olmalı.

## AI2-THOR Etkileri → PDDL Etkileri

- Kamera parametreleri güncellenir.


## PDDL Ön Koşulları

- (camera-active ?c)


## PDDL Etkileri

- (camera-updated ?c)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/UpdateThirdPartyCamera.md`](../ai2thor_api/UpdateThirdPartyCamera.md)
