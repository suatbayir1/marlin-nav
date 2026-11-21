# DirectionalPush → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `DirectionalPush`  
**PDDL Aksiyonu:** `directional-push`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action directional-push
  :parameters (?a - agent ?o - object)
  :precondition (and
    (moveable ?o)
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (in-motion ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Nesne pickupable veya moveable.
- Görünür/erişilebilir.

## AI2-THOR Etkileri → PDDL Etkileri

- Nesne hareket eder.


## PDDL Ön Koşulları

- (moveable ?o)
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (in-motion ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/DirectionalPush.md`](../ai2thor_api/DirectionalPush.md)
