# FillObjectWithLiquid

**Kategori:** Nesne Durumu Değişiklikleri  
**Kaynak:** `raw/object_state_changes.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Boş ve uyumlu nesneyi sıvı ile doldurur.

## Kullanım

```python
controller.step(action="FillObjectWithLiquid", objectId="Mug|0.25|-0.27|0.95", fillLiquid="coffee", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `fillLiquid` | string | Evet | - | coffee, wine veya water. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtı. |

## Ön Koşullar

- canFillWithLiquid=True.
- Boş olmalı.
- Görünür/erişilebilir.

## Etkiler

- isFilledWithLiquid=True
- fillLiquid ayarlanır.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/FillObjectWithLiquid.md`](../pddl_mappings/FillObjectWithLiquid.md)
