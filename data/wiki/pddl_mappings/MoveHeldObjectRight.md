# MoveHeldObjectRight → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `MoveHeldObjectRight`  
**PDDL Aksiyonu:** `move-held-right`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action move-held-right
  :parameters (?a - agent ?o - object)
  :precondition (and
    (holding ?a ?o))
  :effect (and
    (held-offset ?a ?o right))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Ajan nesne tutuyor.

## AI2-THOR Etkileri → PDDL Etkileri

- Tutulan nesne pozisyonu güncellenir.


## PDDL Ön Koşulları

- (holding ?a ?o)


## PDDL Etkileri

- (held-offset ?a ?o right)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/MoveHeldObjectRight.md`](../ai2thor_api/MoveHeldObjectRight.md)
