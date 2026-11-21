# PushObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `PushObject`  
**PDDL Aksiyonu:** `push-object`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action push-object
  :parameters (?a - agent ?o - object)
  :precondition (and
    (moveable ?o)
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (in-motion ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Nesne pickupable veya moveable.

## AI2-THOR Etkileri → PDDL Etkileri

- Nesne ileri itilir.


## PDDL Ön Koşulları

- (moveable ?o)
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (in-motion ?o)


## Notlar

PDDL'de directional-push(?o, 0) ile eşdeğer.

## İlgili API Dokümantasyonu

→ [`ai2thor_api/PushObject.md`](../ai2thor_api/PushObject.md)
