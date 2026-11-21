# SliceObject → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `SliceObject`  
**PDDL Aksiyonu:** `slice-object`  
**Kategori:** Nesne Durumu Değişiklikleri

## PDDL Tanımı

```pddl
(:action slice-object
  :parameters (?a - agent ?o - object)
  :precondition (and
    (sliceable ?o)
    (not (sliced ?o))
    (visible ?o)
    (interactable ?a ?o))
  :effect (and
    (sliced ?o)
    (not (whole ?o)))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- sliceable=True.
- Görünür/erişilebilir.

## AI2-THOR Etkileri → PDDL Etkileri

- isSliced=True
- Yeni dilim nesneleri oluşabilir.


## PDDL Ön Koşulları

- (sliceable ?o)
- (not (sliced ?o))
- (visible ?o)
- (interactable ?a ?o)


## PDDL Etkileri

- (sliced ?o)
- (not (whole ?o))


## İlgili API Dokümantasyonu

→ [`ai2thor_api/SliceObject.md`](../ai2thor_api/SliceObject.md)
