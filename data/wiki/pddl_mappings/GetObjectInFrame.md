# GetObjectInFrame → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `GetObjectInFrame`  
**PDDL Aksiyonu:** `get-object-in-frame`  
**Kategori:** Ortam Sorguları

> **Sorgu aksiyonu:** PDDL'de durum değiştirmez; `actionReturn` sembolik olarak `known(?result)` üretir.

## PDDL Tanımı

```pddl
(:action get-object-in-frame
  :parameters (?a - agent ?o - object)
  :precondition (and
    (in-frame ?o))
  :effect (and
    (increase (total-cost) 0))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- actionReturn: objectId veya None.


## PDDL Ön Koşulları

- (in-frame ?o)


## PDDL Etkileri

_Durum değişikliği yok._

## İlgili API Dokümantasyonu

→ [`ai2thor_api/GetObjectInFrame.md`](../ai2thor_api/GetObjectInFrame.md)
