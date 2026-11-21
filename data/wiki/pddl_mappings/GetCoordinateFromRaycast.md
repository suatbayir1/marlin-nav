# GetCoordinateFromRaycast → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `GetCoordinateFromRaycast`  
**PDDL Aksiyonu:** `get-coordinate-raycast`  
**Kategori:** Ortam Sorguları

> **Sorgu aksiyonu:** PDDL'de durum değiştirmez; `actionReturn` sembolik olarak `known(?result)` üretir.

## PDDL Tanımı

```pddl
(:action get-coordinate-raycast
  :parameters (?a - agent ?p - point)
  
  :effect (and
    (increase (total-cost) 0))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- actionReturn: (x,y,z) koordinat.


## PDDL Ön Koşulları

_Ön koşul yok (sorgu veya kurulum aksiyonu)._

## PDDL Etkileri

_Durum değişikliği yok._

## İlgili API Dokümantasyonu

→ [`ai2thor_api/GetCoordinateFromRaycast.md`](../ai2thor_api/GetCoordinateFromRaycast.md)
