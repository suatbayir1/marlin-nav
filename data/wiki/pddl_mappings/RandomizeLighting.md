# RandomizeLighting → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `RandomizeLighting`  
**PDDL Aksiyonu:** `randomize-lighting`  
**Kategori:** Domain Randomizasyonu

## PDDL Tanımı

```pddl
(:action randomize-lighting
  :parameters ()
  
  :effect (and
    (lighting-randomized))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- Aydınlatma rastgelelenir.


## PDDL Ön Koşulları

_Ön koşul yok (sorgu veya kurulum aksiyonu)._

## PDDL Etkileri

- (lighting-randomized)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/RandomizeLighting.md`](../ai2thor_api/RandomizeLighting.md)
