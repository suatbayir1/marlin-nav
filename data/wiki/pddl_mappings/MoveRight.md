# MoveRight → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `MoveRight`  
**PDDL Aksiyonu:** `move-right`  
**Kategori:** Navigasyon

## PDDL Tanımı

```pddl
(:action move-right
  :parameters (?a - agent ?from - location ?to - location)
  :precondition (and
    (at-agent ?a ?from)
    (adjacent-right ?from ?to)
    (not (blocked-right ?from)))
  :effect (and
    (not (at-agent ?a ?from))
    (at-agent ?a ?to))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Sağda engel olmamalı.

## AI2-THOR Etkileri → PDDL Etkileri

- Ajan pozisyonu güncellenir.


## PDDL Ön Koşulları

- (at-agent ?a ?from)
- (adjacent-right ?from ?to)
- (not (blocked-right ?from))


## PDDL Etkileri

- (not (at-agent ?a ?from))
- (at-agent ?a ?to)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/MoveRight.md`](../ai2thor_api/MoveRight.md)
