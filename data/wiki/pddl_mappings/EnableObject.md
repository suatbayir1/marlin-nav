# EnableObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `EnableObject`  
**PDDL Aksiyonu:** `enable-object`  
**Kategori:** Sahne Kurulumu

## PDDL Tanımı

```pddl
(:action enable-object
  :parameters (?o - object)
  :precondition (and
    (disabled ?o))
  :effect (and
    (not (disabled ?o))
    (enabled ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Nesne disabled durumda.

## AI2-THOR Etkileri → PDDL Etkileri

- Nesne tekrar görünür.
- Orijinal konumuna döner.


## PDDL Ön Koşulları

- (disabled ?o)


## PDDL Etkileri

- (not (disabled ?o))
- (enabled ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/EnableObject.md`](../ai2thor_api/EnableObject.md)
