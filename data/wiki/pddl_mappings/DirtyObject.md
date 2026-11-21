# DirtyObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `DirtyObject`  
**PDDL Aksiyonu:** `dirty-object`  
**Kategori:** Nesne Durumu Değişiklikleri

## PDDL Tanımı

```pddl
(:action dirty-object
  :parameters (?a - agent ?o - object)
  :precondition (and
    (dirtyable ?o)
    (clean ?o)
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (not (clean ?o))
    (dirty ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- dirtyable=True.
- Temiz olmalı.

## AI2-THOR Etkileri → PDDL Etkileri

- isDirty=True


## PDDL Ön Koşulları

- (dirtyable ?o)
- (clean ?o)
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (not (clean ?o))
- (dirty ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/DirtyObject.md`](../ai2thor_api/DirtyObject.md)
