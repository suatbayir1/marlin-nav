# DropHandObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `DropHandObject`  
**PDDL Aksiyonu:** `drop-object`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action drop-object
  :parameters (?a - agent ?o - object ?l - location)
  :precondition (and
    (holding ?a ?o)
    (clear-drop ?a ?o))
  :effect (and
    (not (holding ?a ?o))
    (hand-empty ?a)
    (at-object ?o ?l)
    (on-surface ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Ajan nesne tutuyor.
- Çarpışma engeli yok (forceAction=False).

## AI2-THOR Etkileri → PDDL Etkileri

- Nesne serbest bırakılır.
- isPickedUp=False


## PDDL Ön Koşulları

- (holding ?a ?o)
- (clear-drop ?a ?o)


## PDDL Etkileri

- (not (holding ?a ?o))
- (hand-empty ?a)
- (at-object ?o ?l)
- (on-surface ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/DropHandObject.md`](../ai2thor_api/DropHandObject.md)
