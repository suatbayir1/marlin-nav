# Teleport → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `Teleport`  
**PDDL Aksiyonu:** `teleport`  
**Kategori:** Navigasyon

## PDDL Tanımı

```pddl
(:action teleport
  :parameters (?a - agent ?l - location ?o - orientation)
  :precondition (and
    (reachable-position ?l)
    (valid-pose ?a ?l ?o))
  :effect (and
    (at-agent ?a ?l)
    (facing ?a ?o))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Hedef poz geçerli olmalı (duvar/çarpışma yok).

## AI2-THOR Etkileri → PDDL Etkileri

- Ajan pozu güncellenir.


## PDDL Ön Koşulları

- (reachable-position ?l)
- (valid-pose ?a ?l ?o)


## PDDL Etkileri

- (at-agent ?a ?l)
- (facing ?a ?o)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/Teleport.md`](../ai2thor_api/Teleport.md)
