# MoveAhead → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `MoveAhead`  
**PDDL Aksiyonu:** `move-ahead`  
**Kategori:** Navigasyon

## PDDL Tanımı

```pddl
(:action move-ahead
  :parameters (?a - agent ?from - location ?to - location)
  :precondition (and
    (at-agent ?a ?from)
    (adjacent-forward ?from ?to)
    (hand-empty ?a)
    (not (blocked-forward ?from)))
  :effect (and
    (not (at-agent ?a ?from))
    (at-agent ?a ?to))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Ajanın önünde engel olmamalı.
- snapToGrid=True ise grid noktasına hizalanır.

## AI2-THOR Etkileri → PDDL Etkileri

- Ajan pozisyonu güncellenir.
- Tutulan nesnenin pozisyonu varsayılan konuma sıfırlanır.


## PDDL Ön Koşulları

- (at-agent ?a ?from)
- (adjacent-forward ?from ?to)
- (hand-empty ?a)
- (not (blocked-forward ?from))


## PDDL Etkileri

- (not (at-agent ?a ?from))
- (at-agent ?a ?to)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/MoveAhead.md`](../ai2thor_api/MoveAhead.md)
