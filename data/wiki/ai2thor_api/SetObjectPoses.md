# SetObjectPoses

**Kategori:** Sahne Kurulumu  
**Kaynak:** `raw/set_object_states.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Sahnedeki nesnelerin pozisyon/rotasyonunu toplu ayarlar.

## Kullanım

```python
controller.step(action='SetObjectPoses', objectPoses=[{...}])
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectPoses` | list[dict] | Evet | - | objectName, position, rotation listesi. |

## Ön Koşullar

- Geçerli objectName ve koordinatlar.

## Etkiler

- Belirtilmeyen pickupable/moveable nesneler kaldırılır.
- Nesne pozları güncellenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/SetObjectPoses.md`](../pddl_mappings/SetObjectPoses.md)
