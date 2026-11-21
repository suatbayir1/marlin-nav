# InitialRandomSpawn → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `InitialRandomSpawn`  
**PDDL Aksiyonu:** `initial-random-spawn`  
**Kategori:** Domain Randomizasyonu

## PDDL Tanımı

```pddl
(:action initial-random-spawn
  :parameters ()
  
  :effect (and
    (objects-randomized))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Sahne reset edilmiş olmalı (seed doğruluğu için).

## AI2-THOR Etkileri → PDDL Etkileri

- Nesne pozisyonları değişir.
- objectId'ler yeniden hesaplanır.


## PDDL Ön Koşulları

_Ön koşul yok (sorgu veya kurulum aksiyonu)._

## PDDL Etkileri

- (objects-randomized)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/InitialRandomSpawn.md`](../ai2thor_api/InitialRandomSpawn.md)
