# EmptyLiquidFromObject

**Kategori:** Nesne Durumu Değişiklikleri  
**Kaynak:** `raw/object_state_changes.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Dolu nesnedeki sıvıyı boşaltır.

## Kullanım

```python
controller.step(action="EmptyLiquidFromObject", objectId="Mug|0.25|-0.27|0.95", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtı. |

## Ön Koşullar

- isFilledWithLiquid=True.

## Etkiler

- isFilledWithLiquid=False
- fillLiquid=None


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/EmptyLiquidFromObject.md`](../pddl_mappings/EmptyLiquidFromObject.md)
