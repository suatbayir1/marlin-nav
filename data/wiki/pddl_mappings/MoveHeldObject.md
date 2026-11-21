# MoveHeldObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `MoveHeldObject`  
**PDDL Aksiyonu:** `move-held-object`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action move-held-object
  :parameters (?a - agent ?o - object)
  :precondition (and
    (holding ?a ?o))
  :effect (and
    (held-offset-combined ?a ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Ajan nesne tutuyor.

## AI2-THOR Etkileri → PDDL Etkileri

- Tutulan nesne pozisyonu güncellenir.


## PDDL Ön Koşulları

- (holding ?a ?o)


## PDDL Etkileri

- (held-offset-combined ?a ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/MoveHeldObject.md`](../ai2thor_api/MoveHeldObject.md)
