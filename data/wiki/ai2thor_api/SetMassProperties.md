# SetMassProperties

**Kategori:** Sahne Kurulumu  
**Kaynak:** `raw/set_object_states.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Pickupable/moveable nesnenin kütle özelliklerini değiştirir.

## Kullanım

```python
controller.step(action="SetMassProperties", objectId="Apple|+1.25|+0.25|-0.75", mass=22.5, drag=15.9, angularDrag=5.6)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | str | Evet | - | Hedef nesne. |
| `mass` | float | Evet | - | Kütle (kg, >0). |
| `drag` | float | Evet | - | Sürüklenme katsayısı (>0). |
| `angularDrag` | float | Evet | - | Açısal sürüklenme (>0). |

## Ön Koşullar

- Nesne moveable/pickupable.

## Etkiler

- Kütle özellikleri güncellenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/SetMassProperties.md`](../pddl_mappings/SetMassProperties.md)
