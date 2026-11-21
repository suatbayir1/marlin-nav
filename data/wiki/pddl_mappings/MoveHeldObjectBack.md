# MoveHeldObjectBack → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `MoveHeldObjectBack`  
**PDDL Aksiyonu:** `move-held-back`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action move-held-back
  :parameters (?a - agent ?o - object)
  :precondition (and
    (holding ?a ?o))
  :effect (and
    (held-offset ?a ?o back))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Ajan nesne tutuyor.

## AI2-THOR Etkileri → PDDL Etkileri

- Tutulan nesne pozisyonu güncellenir.


## PDDL Ön Koşulları

- (holding ?a ?o)


## PDDL Etkileri

- (held-offset ?a ?o back)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/MoveHeldObjectBack.md`](../ai2thor_api/MoveHeldObjectBack.md)
