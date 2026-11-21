# MoveLeft

**Kategori:** Navigasyon  
**Kaynak:** `raw/navigation.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Ajanı sola (göreli) hareket ettirir.

## Kullanım

```python
controller.step("MoveLeft")
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `moveMagnitude` | Optional[float] | Hayır | None | Hareket mesafesi (metre). |

## Ön Koşullar

- Solda engel olmamalı.

## Etkiler

- Ajan pozisyonu güncellenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/MoveLeft.md`](../pddl_mappings/MoveLeft.md)
