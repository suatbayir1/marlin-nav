# DisableObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `DisableObject`  
**PDDL Aksiyonu:** `disable-object`  
**Kategori:** Sahne Kurulumu

## PDDL Tanımı

```pddl
(:action disable-object
  :parameters (?o - object)
  :precondition (and
    (exists ?o)
    (enabled ?o))
  :effect (and
    (not (enabled ?o))
    (disabled ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Nesne aktif.

## AI2-THOR Etkileri → PDDL Etkileri

- Nesne devre dışı.
- Destekleyici nesne ise üstündekiler düşebilir.


## PDDL Ön Koşulları

- (exists ?o)
- (enabled ?o)


## PDDL Etkileri

- (not (enabled ?o))
- (disabled ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/DisableObject.md`](../ai2thor_api/DisableObject.md)
