# RotateLeft → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `RotateLeft`  
**PDDL Aksiyonu:** `rotate-left`  
**Kategori:** Navigasyon

## PDDL Tanımı

```pddl
(:action rotate-left
  :parameters (?a - agent ?o - orientation ?n - orientation)
  :precondition (and
    (facing ?a ?o)
    (rotate-left ?o ?n))
  :effect (and
    (not (facing ?a ?o))
    (facing ?a ?n))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- Ajan rotasyonu güncellenir.


## PDDL Ön Koşulları

- (facing ?a ?o)
- (rotate-left ?o ?n)


## PDDL Etkileri

- (not (facing ?a ?o))
- (facing ?a ?n)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/RotateLeft.md`](../ai2thor_api/RotateLeft.md)
