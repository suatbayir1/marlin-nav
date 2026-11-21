# SetMassProperties → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `SetMassProperties`  
**PDDL Aksiyonu:** `set-mass-properties`  
**Kategori:** Sahne Kurulumu

## PDDL Tanımı

```pddl
(:action set-mass-properties
  :parameters (?o - object)
  :precondition (and
    (moveable ?o))
  :effect (and
    (mass-modified ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Nesne moveable/pickupable.

## AI2-THOR Etkileri → PDDL Etkileri

- Kütle özellikleri güncellenir.


## PDDL Ön Koşulları

- (moveable ?o)


## PDDL Etkileri

- (mass-modified ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/SetMassProperties.md`](../ai2thor_api/SetMassProperties.md)
