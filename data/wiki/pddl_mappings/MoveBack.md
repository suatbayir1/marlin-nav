# MoveBack → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `MoveBack`  
**PDDL Aksiyonu:** `move-back`  
**Kategori:** Navigasyon

## PDDL Tanımı

```pddl
(:action move-back
  :parameters (?a - agent ?from - location ?to - location)
  :precondition (and
    (at-agent ?a ?from)
    (adjacent-back ?from ?to)
    (not (blocked-back ?from)))
  :effect (and
    (not (at-agent ?a ?from))
    (at-agent ?a ?to))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Arkada engel olmamalı.

## AI2-THOR Etkileri → PDDL Etkileri

- Ajan pozisyonu güncellenir.


## PDDL Ön Koşulları

- (at-agent ?a ?from)
- (adjacent-back ?from ?to)
- (not (blocked-back ?from))


## PDDL Etkileri

- (not (at-agent ?a ?from))
- (at-agent ?a ?to)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/MoveBack.md`](../ai2thor_api/MoveBack.md)
