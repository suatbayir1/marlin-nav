# ThrowObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `ThrowObject`  
**PDDL Aksiyonu:** `throw-object`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action throw-object
  :parameters (?a - agent ?o - object)
  :precondition (and
    (holding ?a ?o))
  :effect (and
    (not (holding ?a ?o))
    (hand-empty ?a)
    (in-motion ?o)
    (not (on-surface ?o)))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Ajan nesne tutuyor.

## AI2-THOR Etkileri → PDDL Etkileri

- Nesne fırlatılır.
- isPickedUp=False


## PDDL Ön Koşulları

- (holding ?a ?o)


## PDDL Etkileri

- (not (holding ?a ?o))
- (hand-empty ?a)
- (in-motion ?o)
- (not (on-surface ?o))


## İlgili API Dokümantasyonu

→ [`ai2thor_api/ThrowObject.md`](../ai2thor_api/ThrowObject.md)
