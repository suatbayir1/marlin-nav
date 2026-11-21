# LookUp → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `LookUp`  
**PDDL Aksiyonu:** `look-up`  
**Kategori:** Navigasyon

## PDDL Tanımı

```pddl
(:action look-up
  :parameters (?a - agent ?h - horizon ?nh - horizon)
  :precondition (and
    (camera-horizon ?a ?h)
    (look-up ?h ?nh))
  :effect (and
    (not (camera-horizon ?a ?h))
    (camera-horizon ?a ?nh))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- horizon < 60 olmalı.

## AI2-THOR Etkileri → PDDL Etkileri

- cameraHorizon azalır (yukarı bakış).


## PDDL Ön Koşulları

- (camera-horizon ?a ?h)
- (look-up ?h ?nh)


## PDDL Etkileri

- (not (camera-horizon ?a ?h))
- (camera-horizon ?a ?nh)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/LookUp.md`](../ai2thor_api/LookUp.md)
