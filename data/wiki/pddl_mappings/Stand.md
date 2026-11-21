# Stand → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `Stand`  
**PDDL Aksiyonu:** `stand`  
**Kategori:** Navigasyon

## PDDL Tanımı

```pddl
(:action stand
  :parameters (?a - agent)
  :precondition (and
    (crouching ?a))
  :effect (and
    (not (crouching ?a))
    (standing ?a))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Ajan çömelmiş olmalı.

## AI2-THOR Etkileri → PDDL Etkileri

- isStanding=True


## PDDL Ön Koşulları

- (crouching ?a)


## PDDL Etkileri

- (not (crouching ?a))
- (standing ?a)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/Stand.md`](../ai2thor_api/Stand.md)
