# UnpausePhysicsAutoSim → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `UnpausePhysicsAutoSim`  
**PDDL Aksiyonu:** `unpause-physics`  
**Kategori:** Fizik Simülasyonu

## PDDL Tanımı

```pddl
(:action unpause-physics
  :parameters ()
  :precondition (and
    (physics-paused)
    (scene-at-rest))
  :effect (and
    (not (physics-paused))
    (physics-running))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Fizik duraklatılmış.
- Tüm nesneler durmuş olmalı (önerilir).

## AI2-THOR Etkileri → PDDL Etkileri

- Auto-sim açık.


## PDDL Ön Koşulları

- (physics-paused)
- (scene-at-rest)


## PDDL Etkileri

- (not (physics-paused))
- (physics-running)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/UnpausePhysicsAutoSim.md`](../ai2thor_api/UnpausePhysicsAutoSim.md)
