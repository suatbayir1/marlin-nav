# AdvancePhysicsStep → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `AdvancePhysicsStep`  
**PDDL Aksiyonu:** `advance-physics`  
**Kategori:** Fizik Simülasyonu

## PDDL Tanımı

```pddl
(:action advance-physics
  :parameters ()
  :precondition (and
    (physics-paused))
  :effect (and
    (physics-advanced))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- PausePhysicsAutoSim çağrılmış olmalı.

## AI2-THOR Etkileri → PDDL Etkileri

- Fizik durumu timeStep kadar ilerler.


## PDDL Ön Koşulları

- (physics-paused)


## PDDL Etkileri

- (physics-advanced)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/AdvancePhysicsStep.md`](../ai2thor_api/AdvancePhysicsStep.md)
