# Done → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `Done`  
**PDDL Aksiyonu:** `done`  
**Kategori:** Navigasyon

## PDDL Tanımı

```pddl
(:action done
  :parameters (?a - agent)
  :precondition (and
    (goal-achieved))
  :effect (and
    (task-complete))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- Metadata temizlenmiş event döner.


## PDDL Ön Koşulları

- (goal-achieved)


## PDDL Etkileri

- (task-complete)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/Done.md`](../ai2thor_api/Done.md)
