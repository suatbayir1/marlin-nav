# GetReachablePositions → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `GetReachablePositions`  
**PDDL Aksiyonu:** `get-reachable-positions`  
**Kategori:** Ortam Sorguları

> **Sorgu aksiyonu:** PDDL'de durum değiştirmez; `actionReturn` sembolik olarak `known(?result)` üretir.

## PDDL Tanımı

```pddl
(:action get-reachable-positions
  :parameters (?a - agent)
  
  :effect (and
    (increase (total-cost) 0))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- actionReturn: ulaşılabilir pozisyon listesi.


## PDDL Ön Koşulları

_Ön koşul yok (sorgu veya kurulum aksiyonu)._

## PDDL Etkileri

_Durum değişikliği yok._

## İlgili API Dokümantasyonu

→ [`ai2thor_api/GetReachablePositions.md`](../ai2thor_api/GetReachablePositions.md)
