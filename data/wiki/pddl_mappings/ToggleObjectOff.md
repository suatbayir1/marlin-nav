# ToggleObjectOff → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `ToggleObjectOff`  
**PDDL Aksiyonu:** `toggle-off`  
**Kategori:** Nesne Durumu Değişiklikleri

## PDDL Tanımı

```pddl
(:action toggle-off
  :parameters (?a - agent ?o - object)
  :precondition (and
    (toggleable ?o)
    (toggled-on ?o)
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (not (toggled-on ?o))
    (toggled-off ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- toggleable=True.
- Açık olmalı.

## AI2-THOR Etkileri → PDDL Etkileri

- isToggled=False


## PDDL Ön Koşulları

- (toggleable ?o)
- (toggled-on ?o)
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (not (toggled-on ?o))
- (toggled-off ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/ToggleObjectOff.md`](../ai2thor_api/ToggleObjectOff.md)
