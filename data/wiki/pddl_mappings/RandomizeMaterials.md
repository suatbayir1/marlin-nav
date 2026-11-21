# RandomizeMaterials → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `RandomizeMaterials`  
**PDDL Aksiyonu:** `randomize-materials`  
**Kategori:** Domain Randomizasyonu

## PDDL Tanımı

```pddl
(:action randomize-materials
  :parameters ()
  
  :effect (and
    (materials-randomized))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- Malzemeler rastgelelenir.
- Reset ile eski haline döner.


## PDDL Ön Koşulları

_Ön koşul yok (sorgu veya kurulum aksiyonu)._

## PDDL Etkileri

- (materials-randomized)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/RandomizeMaterials.md`](../ai2thor_api/RandomizeMaterials.md)
