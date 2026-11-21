# PausePhysicsAutoSim → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `PausePhysicsAutoSim`  
**PDDL Aksiyonu:** `pause-physics`  
**Kategori:** Fizik Simülasyonu

## PDDL Tanımı

```pddl
(:action pause-physics
  :parameters ()
  :precondition (and
    (physics-running))
  :effect (and
    (not (physics-running))
    (physics-paused))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- Auto-sim kapalı.
- AdvancePhysicsStep kullanılabilir.


## PDDL Ön Koşulları

- (physics-running)


## PDDL Etkileri

- (not (physics-running))
- (physics-paused)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/PausePhysicsAutoSim.md`](../ai2thor_api/PausePhysicsAutoSim.md)
