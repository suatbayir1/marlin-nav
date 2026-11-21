# SetDecayTemperatureBool → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `SetDecayTemperatureBool`  
**PDDL Aksiyonu:** `set-decay-temp-bool`  
**Kategori:** Sahne Kurulumu

## PDDL Tanımı

```pddl
(:action set-decay-temp-bool
  :parameters ()
  
  :effect (and
    (temp-decay-enabled))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- Sıcaklık decay davranışı değişir.


## PDDL Ön Koşulları

_Ön koşul yok (sorgu veya kurulum aksiyonu)._

## PDDL Etkileri

- (temp-decay-enabled)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/SetDecayTemperatureBool.md`](../ai2thor_api/SetDecayTemperatureBool.md)
