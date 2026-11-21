# MoveAhead

**Kategori:** Navigasyon  
**Kaynak:** `raw/navigation.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Ajanı ileri yönde (baktığı yöne) hareket ettirir.

## Kullanım

```python
controller.step(action="MoveAhead", moveMagnitude=None)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `moveMagnitude` | Optional[float] | Hayır | None | gridSize varsayılanını geçersiz kılar (metre). |

## Ön Koşullar

- Ajanın önünde engel olmamalı.
- snapToGrid=True ise grid noktasına hizalanır.

## Etkiler

- Ajan pozisyonu güncellenir.
- Tutulan nesnenin pozisyonu varsayılan konuma sıfırlanır.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/MoveAhead.md`](../pddl_mappings/MoveAhead.md)
