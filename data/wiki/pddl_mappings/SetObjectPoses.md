# SetObjectPoses → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `SetObjectPoses`  
**PDDL Aksiyonu:** `set-object-poses`  
**Kategori:** Sahne Kurulumu

## PDDL Tanımı

```pddl
(:action set-object-poses
  :parameters (?o - object ?p - point ?r - rotation)
  
  :effect (and
    (at-point ?o ?p)
    (object-rotation ?o ?r))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

- Geçerli objectName ve koordinatlar.

## AI2-THOR Etkileri → PDDL Etkileri

- Belirtilmeyen pickupable/moveable nesneler kaldırılır.
- Nesne pozları güncellenir.


## PDDL Ön Koşulları

_Ön koşul yok (sorgu veya kurulum aksiyonu)._

## PDDL Etkileri

- (at-point ?o ?p)
- (object-rotation ?o ?r)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/SetObjectPoses.md`](../ai2thor_api/SetObjectPoses.md)
