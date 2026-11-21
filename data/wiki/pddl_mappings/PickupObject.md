# PickupObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `PickupObject`  
**PDDL Aksiyonu:** `pickup-object`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action pickup-object
  :parameters (?a - agent ?o - object)
  :precondition (and
    (pickupable ?o)
    (hand-empty ?a)
    (visible ?o)
    (interactable ?a ?o)
    (not (holding ?a ?o)))
  :effect (and
    (holding ?a ?o)
    (not (hand-empty ?a))
    (not (on-surface ?o)))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Nesne pickupable=True.
- Ajan eli boş.
- Nesne görünür/erişilebilir.
- Çarpışma yok.

## AI2-THOR Etkileri → PDDL Etkileri

- isPickedUp=True
- İçerdiği nesneler de birlikte alınabilir (receptacle).


## PDDL Ön Koşulları

- (pickupable ?o)
- (hand-empty ?a)
- (visible ?o)
- (interactable ?a ?o)
- (not (holding ?a ?o))


## PDDL Etkileri

- (holding ?a ?o)
- (not (hand-empty ?a))
- (not (on-surface ?o))


## İlgili API Dokümantasyonu

→ [`ai2thor_api/PickupObject.md`](../ai2thor_api/PickupObject.md)
