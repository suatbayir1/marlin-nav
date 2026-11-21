# TeleportFull → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `TeleportFull`  
**PDDL Aksiyonu:** `teleport-full`  
**Kategori:** Navigasyon

## PDDL Tanımı

```pddl
(:action teleport-full
  :parameters (?a - agent ?l - location ?o - orientation ?h - horizon)
  :precondition (and
    (reachable-position ?l)
    (valid-full-pose ?a ?l ?o ?h))
  :effect (and
    (at-agent ?a ?l)
    (facing ?a ?o)
    (camera-horizon ?a ?h))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Tüm parametreler geçerli olmalı.

## AI2-THOR Etkileri → PDDL Etkileri

- Ajan pozu tam olarak ayarlanır.


## PDDL Ön Koşulları

- (reachable-position ?l)
- (valid-full-pose ?a ?l ?o ?h)


## PDDL Etkileri

- (at-agent ?a ?l)
- (facing ?a ?o)
- (camera-horizon ?a ?h)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/TeleportFull.md`](../ai2thor_api/TeleportFull.md)
