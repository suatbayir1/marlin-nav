# ToggleObjectOn → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `ToggleObjectOn`  
**PDDL Aksiyonu:** `toggle-on`  
**Kategori:** Nesne Durumu Değişiklikleri

## PDDL Tanımı

```pddl
(:action toggle-on
  :parameters (?a - agent ?o - object)
  :precondition (and
    (toggleable ?o)
    (toggled-off ?o)
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (not (toggled-off ?o))
    (toggled-on ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- toggleable=True.
- Kapalı olmalı.
- Görünür/erişilebilir.

## AI2-THOR Etkileri → PDDL Etkileri

- isToggled=True


## PDDL Ön Koşulları

- (toggleable ?o)
- (toggled-off ?o)
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (not (toggled-off ?o))
- (toggled-on ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/ToggleObjectOn.md`](../ai2thor_api/ToggleObjectOn.md)
