# SetRoomTempDecayTimeForType → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `SetRoomTempDecayTimeForType`  
**PDDL Aksiyonu:** `set-temp-decay-type`  
**Kategori:** Sahne Kurulumu

## PDDL Tanımı

```pddl
(:action set-temp-decay-type
  :parameters (?t - objecttype)
  
  :effect (and
    (temp-decay-time ?t))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- Tip bazlı sıcaklık decay süresi güncellenir.


## PDDL Ön Koşulları

_Ön koşul yok (sorgu veya kurulum aksiyonu)._

## PDDL Etkileri

- (temp-decay-time ?t)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/SetRoomTempDecayTimeForType.md`](../ai2thor_api/SetRoomTempDecayTimeForType.md)
