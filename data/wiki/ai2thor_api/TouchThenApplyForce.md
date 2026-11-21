# TouchThenApplyForce

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Ekran koordinatından ışın göndererek nesneye kuvvet uygular.

## Kullanım

```python
controller.step(action="TouchThenApplyForce", x=0.5, y=0.5, direction={"x":0,"y":1,"z":0}, moveMagnitude=80, handDistance=1.5)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `x` | float | Evet | - | Ekran x [0:1]. |
| `y` | float | Evet | - | Ekran y [0:1]. |
| `direction` | dict | Evet | - | İtme yön vektörü {x,y,z}. |
| `moveMagnitude` | float | Evet | - | Kuvvet (newton). |
| `handDistance` | float | Evet | - | Maksimum el mesafesi (metre). |

## Ön Koşullar

- Hedef görünür ve handDistance içinde.
- pickupable/moveable nesne.

## Etkiler

- Nesneye anlık kuvvet uygulanır.
- actionReturn geri bildirim döner.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/TouchThenApplyForce.md`](../pddl_mappings/TouchThenApplyForce.md)
