# BreakObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `BreakObject`  
**PDDL Aksiyonu:** `break-object`  
**Kategori:** Nesne Durumu Değişiklikleri

## PDDL Tanımı

```pddl
(:action break-object
  :parameters (?a - agent ?o - object)
  :precondition (and
    (breakable ?o)
    (not (broken ?o))
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (broken ?o)
    (not (intact ?o)))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- breakable=True.
- Görünür/erişilebilir.

## AI2-THOR Etkileri → PDDL Etkileri

- isBroken=True


## PDDL Ön Koşulları

- (breakable ?o)
- (not (broken ?o))
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (broken ?o)
- (not (intact ?o))


## İlgili API Dokümantasyonu

→ [`ai2thor_api/BreakObject.md`](../ai2thor_api/BreakObject.md)
