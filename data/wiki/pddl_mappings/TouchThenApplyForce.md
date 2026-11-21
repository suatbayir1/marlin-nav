# TouchThenApplyForce → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `TouchThenApplyForce`  
**PDDL Aksiyonu:** `touch-apply-force`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action touch-apply-force
  :parameters (?a - agent ?o - object)
  :precondition (and
    (visible ?o)
    (in-range ?a ?o)
    (moveable ?o))
  :effect (and
    (in-motion ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Hedef görünür ve handDistance içinde.
- pickupable/moveable nesne.

## AI2-THOR Etkileri → PDDL Etkileri

- Nesneye anlık kuvvet uygulanır.
- actionReturn geri bildirim döner.


## PDDL Ön Koşulları

- (visible ?o)
- (in-range ?a ?o)
- (moveable ?o)


## PDDL Etkileri

- (in-motion ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/TouchThenApplyForce.md`](../ai2thor_api/TouchThenApplyForce.md)
