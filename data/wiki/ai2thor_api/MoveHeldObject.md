# MoveHeldObject

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Tutulan nesneyi ahead/right/up eksenlerinde tek aksiyonla hareket ettirir.

## Kullanım

```python
controller.step(action="MoveHeldObject", ahead=0.1, right=0.05, up=0.12, forceVisible=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `ahead` | float | Evet | - | İleri mesafe (metre). |
| `right` | float | Evet | - | Sağ mesafe (metre). |
| `up` | float | Evet | - | Yukarı mesafe (metre). |
| `forceVisible` | bool | Hayır | False | Görünürlük zorunluluğu. |

## Ön Koşullar

- Ajan nesne tutuyor.

## Etkiler

- Tutulan nesne pozisyonu güncellenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/MoveHeldObject.md`](../pddl_mappings/MoveHeldObject.md)
