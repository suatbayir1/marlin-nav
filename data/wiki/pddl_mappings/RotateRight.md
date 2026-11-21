# RotateRight → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `RotateRight`  
**PDDL Aksiyonu:** `rotate-right`  
**Kategori:** Navigasyon

## PDDL Tanımı

```pddl
(:action rotate-right
  :parameters (?a - agent ?o - orientation ?n - orientation)
  :precondition (and
    (facing ?a ?o)
    (rotate-right ?o ?n))
  :effect (and
    (not (facing ?a ?o))
    (facing ?a ?n))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- Ajan rotasyonu güncellenir.
- Tutulan nesne rotasyonu sıfırlanır.


## PDDL Ön Koşulları

- (facing ?a ?o)
- (rotate-right ?o ?n)


## PDDL Etkileri

- (not (facing ?a ?o))
- (facing ?a ?n)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/RotateRight.md`](../ai2thor_api/RotateRight.md)
