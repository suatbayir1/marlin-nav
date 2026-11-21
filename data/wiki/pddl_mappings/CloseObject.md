# CloseObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `CloseObject`  
**PDDL Aksiyonu:** `close-object`  
**Kategori:** Nesne Durumu Değişiklikleri

## PDDL Tanımı

```pddl
(:action close-object
  :parameters (?a - agent ?o - object)
  :precondition (and
    (openable ?o)
    (open ?o)
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (not (open ?o))
    (closed ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- openable=True.
- Açık olmalı.

## AI2-THOR Etkileri → PDDL Etkileri

- openness=0.
- isOpen=False


## PDDL Ön Koşulları

- (openable ?o)
- (open ?o)
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (not (open ?o))
- (closed ?o)


## Notlar

PDDL'de open-object(?o, 0) ile eşdeğer.

## İlgili API Dokümantasyonu

→ [`ai2thor_api/CloseObject.md`](../ai2thor_api/CloseObject.md)
