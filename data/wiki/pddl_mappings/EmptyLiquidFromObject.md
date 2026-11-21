# EmptyLiquidFromObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `EmptyLiquidFromObject`  
**PDDL Aksiyonu:** `empty-liquid`  
**Kategori:** Nesne Durumu Değişiklikleri

## PDDL Tanımı

```pddl
(:action empty-liquid
  :parameters (?a - agent ?o - object ?l - liquid)
  :precondition (and
    (filled-with ?o ?l)
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (not (filled-with ?o ?l))
    (empty-liquid ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- isFilledWithLiquid=True.

## AI2-THOR Etkileri → PDDL Etkileri

- isFilledWithLiquid=False
- fillLiquid=None


## PDDL Ön Koşulları

- (filled-with ?o ?l)
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (not (filled-with ?o ?l))
- (empty-liquid ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/EmptyLiquidFromObject.md`](../ai2thor_api/EmptyLiquidFromObject.md)
