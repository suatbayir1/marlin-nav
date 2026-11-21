# GetSpawnCoordinatesAboveReceptacle → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `GetSpawnCoordinatesAboveReceptacle`  
**PDDL Aksiyonu:** `get-spawn-coordinates`  
**Kategori:** Ortam Sorguları

> **Sorgu aksiyonu:** PDDL'de durum değiştirmez; `actionReturn` sembolik olarak `known(?result)` üretir.

## PDDL Tanımı

```pddl
(:action get-spawn-coordinates
  :parameters (?r - receptacle)
  :precondition (and
    (receptacle ?r))
  :effect (and
    (increase (total-cost) 0))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- actionReturn: xyz koordinat listesi.


## PDDL Ön Koşulları

- (receptacle ?r)


## PDDL Etkileri

_Durum değişikliği yok._

## İlgili API Dokümantasyonu

→ [`ai2thor_api/GetSpawnCoordinatesAboveReceptacle.md`](../ai2thor_api/GetSpawnCoordinatesAboveReceptacle.md)
