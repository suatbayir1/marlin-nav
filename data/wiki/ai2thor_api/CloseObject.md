# CloseObject

**Kategori:** Nesne Durumu Değişiklikleri  
**Kaynak:** `raw/object_state_changes.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

OpenObject'un openness=0 sözdizimsel kısayolu.

## Kullanım

```python
controller.step(action="CloseObject", objectId="Book|0.25|-0.27|0.95", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtını yok sayar. |

## Ön Koşullar

- openable=True.
- Açık olmalı.

## Etkiler

- openness=0.
- isOpen=False


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/CloseObject.md`](../pddl_mappings/CloseObject.md)
