# MoveHeldObjectLeft

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Tutulan nesneyi sola hareket ettirir.

## Kullanım

```python
controller.step("MoveHeldObjectLeft")
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `moveMagnitude` | float | Evet | - | Hareket mesafesi (metre). |
| `forceVisible` | bool | Hayır | False | Görünürlük zorunluluğu. |

## Ön Koşullar

- Ajan nesne tutuyor.

## Etkiler

- Tutulan nesne pozisyonu güncellenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/MoveHeldObjectLeft.md`](../pddl_mappings/MoveHeldObjectLeft.md)
