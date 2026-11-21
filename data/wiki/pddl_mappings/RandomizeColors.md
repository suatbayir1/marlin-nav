# RandomizeColors → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `RandomizeColors`  
**PDDL Aksiyonu:** `randomize-colors`  
**Kategori:** Domain Randomizasyonu

## PDDL Tanımı

```pddl
(:action randomize-colors
  :parameters ()
  
  :effect (and
    (colors-randomized))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- Nesne renkleri rastgelelenir.


## PDDL Ön Koşulları

_Ön koşul yok (sorgu veya kurulum aksiyonu)._

## PDDL Etkileri

- (colors-randomized)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/RandomizeColors.md`](../ai2thor_api/RandomizeColors.md)
