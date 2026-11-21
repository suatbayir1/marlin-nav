# CookObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `CookObject`  
**PDDL Aksiyonu:** `cook-object`  
**Kategori:** Nesne Durumu Değişiklikleri

## PDDL Tanımı

```pddl
(:action cook-object
  :parameters (?a - agent ?o - object)
  :precondition (and
    (cookable ?o)
    (not (cooked ?o))
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (cooked ?o)
    (not (raw ?o)))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- cookable=True.
- Görünür/erişilebilir.

## AI2-THOR Etkileri → PDDL Etkileri

- isCooked=True


## PDDL Ön Koşulları

- (cookable ?o)
- (not (cooked ?o))
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (cooked ?o)
- (not (raw ?o))


## İlgili API Dokümantasyonu

→ [`ai2thor_api/CookObject.md`](../ai2thor_api/CookObject.md)
