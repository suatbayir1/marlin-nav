# DirtyObject

**Kategori:** Nesne Durumu Değişiklikleri  
**Kaynak:** `raw/object_state_changes.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Kirletilebilir nesneyi kirli yapar.

## Kullanım

```python
controller.step(action="DirtyObject", objectId="Mug|0.25|-0.27|0.95", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtı. |

## Ön Koşullar

- dirtyable=True.
- Temiz olmalı.

## Etkiler

- isDirty=True


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/DirtyObject.md`](../pddl_mappings/DirtyObject.md)
