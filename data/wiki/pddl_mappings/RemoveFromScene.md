# RemoveFromScene → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `RemoveFromScene`  
**PDDL Aksiyonu:** `remove-from-scene`  
**Kategori:** Sahne Kurulumu

## PDDL Tanımı

```pddl
(:action remove-from-scene
  :parameters (?o - object)
  :precondition (and
    (exists ?o))
  :effect (and
    (not (exists ?o)))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Nesne sahnede mevcut.

## AI2-THOR Etkileri → PDDL Etkileri

- Nesne yok edilir (reset gerekir).


## PDDL Ön Koşulları

- (exists ?o)


## PDDL Etkileri

- (not (exists ?o))


## İlgili API Dokümantasyonu

→ [`ai2thor_api/RemoveFromScene.md`](../ai2thor_api/RemoveFromScene.md)
