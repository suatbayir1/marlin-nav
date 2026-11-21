# Crouch → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `Crouch`  
**PDDL Aksiyonu:** `crouch`  
**Kategori:** Navigasyon

## PDDL Tanımı

```pddl
(:action crouch
  :parameters (?a - agent)
  :precondition (and
    (standing ?a))
  :effect (and
    (not (standing ?a))
    (crouching ?a))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Ajan ayakta olmalı (isStanding=True).

## AI2-THOR Etkileri → PDDL Etkileri

- isStanding=False


## PDDL Ön Koşulları

- (standing ?a)


## PDDL Etkileri

- (not (standing ?a))
- (crouching ?a)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/Crouch.md`](../ai2thor_api/Crouch.md)
