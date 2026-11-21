# CleanObject

**Kategori:** Nesne Durumu Değişiklikleri  
**Kaynak:** `raw/object_state_changes.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Kirli nesneyi temizler.

## Kullanım

```python
controller.step(action="CleanObject", objectId="Mug|0.25|-0.27|0.95", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtı. |

## Ön Koşullar

- dirtyable=True.
- Kirli olmalı.

## Etkiler

- isDirty=False


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/CleanObject.md`](../pddl_mappings/CleanObject.md)
