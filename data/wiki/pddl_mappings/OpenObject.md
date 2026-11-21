# OpenObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `OpenObject`  
**PDDL Aksiyonu:** `open-object`  
**Kategori:** Nesne Durumu Değişiklikleri

## PDDL Tanımı

```pddl
(:action open-object
  :parameters (?a - agent ?o - object)
  :precondition (and
    (openable ?o)
    (closed ?o)
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (not (closed ?o))
    (open ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- openable=True.
- Görünür/erişilebilir.
- Çarpışma engeli yok.

## AI2-THOR Etkileri → PDDL Etkileri

- openness güncellenir.
- isOpen=True (openness>0).


## PDDL Ön Koşulları

- (openable ?o)
- (closed ?o)
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (not (closed ?o))
- (open ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/OpenObject.md`](../ai2thor_api/OpenObject.md)
