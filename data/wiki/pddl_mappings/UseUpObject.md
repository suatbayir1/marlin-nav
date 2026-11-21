# UseUpObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `UseUpObject`  
**PDDL Aksiyonu:** `use-up-object`  
**Kategori:** Nesne Durumu Değişiklikleri

## PDDL Tanımı

```pddl
(:action use-up-object
  :parameters (?a - agent ?o - object)
  :precondition (and
    (can-be-used-up ?o)
    (not (used-up ?o))
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (used-up ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- canBeUsedUp=True.
- Tükenmemiş olmalı.

## AI2-THOR Etkileri → PDDL Etkileri

- isUsedUp=True (veya kısmi tüketim).


## PDDL Ön Koşulları

- (can-be-used-up ?o)
- (not (used-up ?o))
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (used-up ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/UseUpObject.md`](../ai2thor_api/UseUpObject.md)
