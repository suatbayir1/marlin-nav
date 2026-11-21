# MoveHeldObjectUp → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `MoveHeldObjectUp`  
**PDDL Aksiyonu:** `move-held-up`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action move-held-up
  :parameters (?a - agent ?o - object)
  :precondition (and
    (holding ?a ?o))
  :effect (and
    (held-offset ?a ?o up))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Ajan nesne tutuyor.

## AI2-THOR Etkileri → PDDL Etkileri

- Tutulan nesne pozisyonu güncellenir.


## PDDL Ön Koşulları

- (holding ?a ?o)


## PDDL Etkileri

- (held-offset ?a ?o up)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/MoveHeldObjectUp.md`](../ai2thor_api/MoveHeldObjectUp.md)
