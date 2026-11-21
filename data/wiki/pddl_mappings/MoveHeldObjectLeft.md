# MoveHeldObjectLeft → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `MoveHeldObjectLeft`  
**PDDL Aksiyonu:** `move-held-left`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action move-held-left
  :parameters (?a - agent ?o - object)
  :precondition (and
    (holding ?a ?o))
  :effect (and
    (held-offset ?a ?o left))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Ajan nesne tutuyor.

## AI2-THOR Etkileri → PDDL Etkileri

- Tutulan nesne pozisyonu güncellenir.


## PDDL Ön Koşulları

- (holding ?a ?o)


## PDDL Etkileri

- (held-offset ?a ?o left)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/MoveHeldObjectLeft.md`](../ai2thor_api/MoveHeldObjectLeft.md)
