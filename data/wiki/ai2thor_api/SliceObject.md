# SliceObject

**Kategori:** Nesne Durumu Değişiklikleri  
**Kaynak:** `raw/object_state_changes.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Dilimlenebilir nesneyi dilimler; yeni dilim nesneleri oluşabilir.

## Kullanım

```python
controller.step(action="SliceObject", objectId="Potato|0.25|-0.27|0.95", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtı. |

## Ön Koşullar

- sliceable=True.
- Görünür/erişilebilir.

## Etkiler

- isSliced=True
- Yeni dilim nesneleri oluşabilir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/SliceObject.md`](../pddl_mappings/SliceObject.md)
