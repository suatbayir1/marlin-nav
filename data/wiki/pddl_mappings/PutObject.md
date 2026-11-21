# PutObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `PutObject`  
**PDDL Aksiyonu:** `put-object`  
**Kategori:** Etkileşim / Manipülasyon

## PDDL Tanımı

```pddl
(:action put-object
  :parameters (?a - agent ?o - object ?r - receptacle)
  :precondition (and
    (holding ?a ?o)
    (receptacle ?r)
    (valid-receptacle-for ?o ?r)
    (visible ?r))
  :effect (and
    (not (holding ?a ?o))
    (hand-empty ?a)
    (in-receptacle ?o ?r)
    (on-surface ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Ajan nesne tutuyor.
- Hedef receptacle=True.
- Geçerli receptacle kısıtları.

## AI2-THOR Etkileri → PDDL Etkileri

- Nesne receptacle'a yerleşir.
- isPickedUp=False


## PDDL Ön Koşulları

- (holding ?a ?o)
- (receptacle ?r)
- (valid-receptacle-for ?o ?r)
- (visible ?r)


## PDDL Etkileri

- (not (holding ?a ?o))
- (hand-empty ?a)
- (in-receptacle ?o ?r)
- (on-surface ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/PutObject.md`](../ai2thor_api/PutObject.md)
