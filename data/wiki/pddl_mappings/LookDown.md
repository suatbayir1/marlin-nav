# LookDown → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `LookDown`  
**PDDL Aksiyonu:** `look-down`  
**Kategori:** Navigasyon

## PDDL Tanımı

```pddl
(:action look-down
  :parameters (?a - agent ?h - horizon ?nh - horizon)
  :precondition (and
    (camera-horizon ?a ?h)
    (look-down ?h ?nh))
  :effect (and
    (not (camera-horizon ?a ?h))
    (camera-horizon ?a ?nh))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- horizon > -30 olmalı.

## AI2-THOR Etkileri → PDDL Etkileri

- cameraHorizon artar (aşağı bakış).


## PDDL Ön Koşulları

- (camera-horizon ?a ?h)
- (look-down ?h ?nh)


## PDDL Etkileri

- (not (camera-horizon ?a ?h))
- (camera-horizon ?a ?nh)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/LookDown.md`](../ai2thor_api/LookDown.md)
