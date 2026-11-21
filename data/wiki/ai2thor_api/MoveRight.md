# MoveRight

**Kategori:** Navigasyon  
**Kaynak:** `raw/navigation.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Ajanı sağa (göreli) hareket ettirir.

## Kullanım

```python
controller.step("MoveRight")
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `moveMagnitude` | Optional[float] | Hayır | None | Hareket mesafesi (metre). |

## Ön Koşullar

- Sağda engel olmamalı.

## Etkiler

- Ajan pozisyonu güncellenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/MoveRight.md`](../pddl_mappings/MoveRight.md)
