# MoveLeft → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `MoveLeft`  
**PDDL Aksiyonu:** `move-left`  
**Kategori:** Navigasyon

## PDDL Tanımı

```pddl
(:action move-left
  :parameters (?a - agent ?from - location ?to - location)
  :precondition (and
    (at-agent ?a ?from)
    (adjacent-left ?from ?to)
    (not (blocked-left ?from)))
  :effect (and
    (not (at-agent ?a ?from))
    (at-agent ?a ?to))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Solda engel olmamalı.

## AI2-THOR Etkileri → PDDL Etkileri

- Ajan pozisyonu güncellenir.


## PDDL Ön Koşulları

- (at-agent ?a ?from)
- (adjacent-left ?from ?to)
- (not (blocked-left ?from))


## PDDL Etkileri

- (not (at-agent ?a ?from))
- (at-agent ?a ?to)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/MoveLeft.md`](../ai2thor_api/MoveLeft.md)
