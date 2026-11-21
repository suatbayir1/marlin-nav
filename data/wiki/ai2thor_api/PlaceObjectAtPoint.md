# PlaceObjectAtPoint

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Nesneyi belirtilen global koordinata receptacle yüzeyine yerleştirir.

## Kullanım

```python
controller.step(action="PlaceObjectAtPoint", objectId="Toaster|1|1|1", position={"x":-1.25,"y":1.0,"z":-1.0})
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Yerleştirilecek nesne. |
| `position` | dict | Evet | - | Global (x,y,z) koordinat. |

## Ön Koşullar

- Nesne pickupable veya moveable.
- Geçerli yerleşim noktası.

## Etkiler

- Nesne belirtilen noktaya teleport edilir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/PlaceObjectAtPoint.md`](../pddl_mappings/PlaceObjectAtPoint.md)
