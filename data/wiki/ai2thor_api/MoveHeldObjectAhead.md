# MoveHeldObjectAhead

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Tutulan nesneyi ileri yönde hareket ettirir.

## Kullanım

```python
controller.step(action="MoveHeldObjectAhead", moveMagnitude=0.1, forceVisible=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `moveMagnitude` | float | Evet | - | Hareket mesafesi (metre). |
| `forceVisible` | bool | Hayır | False | True ise nesne görünür kalmalı. |

## Ön Koşullar

- Ajan nesne tutuyor.

## Etkiler

- Tutulan nesne pozisyonu güncellenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/MoveHeldObjectAhead.md`](../pddl_mappings/MoveHeldObjectAhead.md)
