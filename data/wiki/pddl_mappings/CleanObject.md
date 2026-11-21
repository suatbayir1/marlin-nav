# CleanObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `CleanObject`  
**PDDL Aksiyonu:** `clean-object`  
**Kategori:** Nesne Durumu Değişiklikleri

## PDDL Tanımı

```pddl
(:action clean-object
  :parameters (?a - agent ?o - object)
  :precondition (and
    (dirtyable ?o)
    (dirty ?o)
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (not (dirty ?o))
    (clean ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- dirtyable=True.
- Kirli olmalı.

## AI2-THOR Etkileri → PDDL Etkileri

- isDirty=False


## PDDL Ön Koşulları

- (dirtyable ?o)
- (dirty ?o)
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (not (dirty ?o))
- (clean ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/CleanObject.md`](../ai2thor_api/CleanObject.md)
