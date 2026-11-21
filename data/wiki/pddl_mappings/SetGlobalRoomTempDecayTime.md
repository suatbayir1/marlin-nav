# SetGlobalRoomTempDecayTime → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `SetGlobalRoomTempDecayTime`  
**PDDL Aksiyonu:** `set-global-temp-decay`  
**Kategori:** Sahne Kurulumu

## PDDL Tanımı

```pddl
(:action set-global-temp-decay
  :parameters ()
  
  :effect (and
    (global-temp-decay-set))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- Global decay süresi güncellenir.


## PDDL Ön Koşulları

_Ön koşul yok (sorgu veya kurulum aksiyonu)._

## PDDL Etkileri

- (global-temp-decay-set)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/SetGlobalRoomTempDecayTime.md`](../ai2thor_api/SetGlobalRoomTempDecayTime.md)
