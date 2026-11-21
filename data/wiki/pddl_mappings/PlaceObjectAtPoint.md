# PlaceObjectAtPoint → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `PlaceObjectAtPoint`  
**PDDL Aksiyonu:** `place-at-point`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action place-at-point
  :parameters (?o - object ?p - point)
  :precondition (and
    (pickupable ?o)
    (valid-placement-point ?o ?p))
  :effect (and
    (at-point ?o ?p)
    (on-surface ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Nesne pickupable veya moveable.
- Geçerli yerleşim noktası.

## AI2-THOR Etkileri → PDDL Etkileri

- Nesne belirtilen noktaya teleport edilir.


## PDDL Ön Koşulları

- (pickupable ?o)
- (valid-placement-point ?o ?p)


## PDDL Etkileri

- (at-point ?o ?p)
- (on-surface ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/PlaceObjectAtPoint.md`](../ai2thor_api/PlaceObjectAtPoint.md)
