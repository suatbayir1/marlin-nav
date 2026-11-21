# MoveBack

**Kategori:** Navigasyon  
**Kaynak:** `raw/navigation.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Ajanı geri yönde hareket ettirir.

## Kullanım

```python
controller.step("MoveBack")
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `moveMagnitude` | Optional[float] | Hayır | None | Hareket mesafesi (metre). |

## Ön Koşullar

- Arkada engel olmamalı.

## Etkiler

- Ajan pozisyonu güncellenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/MoveBack.md`](../pddl_mappings/MoveBack.md)
