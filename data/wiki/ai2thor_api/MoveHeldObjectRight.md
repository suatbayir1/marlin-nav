# MoveHeldObjectRight

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Tutulan nesneyi sağa hareket ettirir.

## Kullanım

```python
controller.step("MoveHeldObjectRight")
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

→ [`pddl_mappings/MoveHeldObjectRight.md`](../pddl_mappings/MoveHeldObjectRight.md)
