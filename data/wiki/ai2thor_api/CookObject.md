# CookObject

**Kategori:** Nesne Durumu Değişiklikleri  
**Kaynak:** `raw/object_state_changes.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Pişirilebilir nesneyi pişirir (geri alınamaz).

## Kullanım

```python
controller.step(action="CookObject", objectId="Egg|0.25|-0.27|0.95", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtı. |

## Ön Koşullar

- cookable=True.
- Görünür/erişilebilir.

## Etkiler

- isCooked=True


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/CookObject.md`](../pddl_mappings/CookObject.md)
