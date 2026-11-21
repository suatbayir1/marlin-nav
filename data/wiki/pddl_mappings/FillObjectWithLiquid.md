# FillObjectWithLiquid → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `FillObjectWithLiquid`  
**PDDL Aksiyonu:** `fill-liquid`  
**Kategori:** Nesne Durumu Değişiklikleri

## PDDL Tanımı

```pddl
(:action fill-liquid
  :parameters (?a - agent ?o - object ?l - liquid)
  :precondition (and
    (can-fill ?o)
    (empty-liquid ?o)
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (not (empty-liquid ?o))
    (filled-with ?o ?l))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- canFillWithLiquid=True.
- Boş olmalı.
- Görünür/erişilebilir.

## AI2-THOR Etkileri → PDDL Etkileri

- isFilledWithLiquid=True
- fillLiquid ayarlanır.


## PDDL Ön Koşulları

- (can-fill ?o)
- (empty-liquid ?o)
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (not (empty-liquid ?o))
- (filled-with ?o ?l)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/FillObjectWithLiquid.md`](../ai2thor_api/FillObjectWithLiquid.md)
