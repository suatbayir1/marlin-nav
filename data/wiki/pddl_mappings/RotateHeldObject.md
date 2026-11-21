# RotateHeldObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `RotateHeldObject`  
**PDDL Aksiyonu:** `rotate-held-object`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action rotate-held-object
  :parameters (?a - agent ?o - object)
  :precondition (and
    (holding ?a ?o))
  :effect (and
    (held-rotated ?a ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Ajan nesne tutuyor.

## AI2-THOR Etkileri → PDDL Etkileri

- Tutulan nesne rotasyonu güncellenir.


## PDDL Ön Koşulları

- (holding ?a ?o)


## PDDL Etkileri

- (held-rotated ?a ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/RotateHeldObject.md`](../ai2thor_api/RotateHeldObject.md)
