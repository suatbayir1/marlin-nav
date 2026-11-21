# RotateHeldObject

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Tutulan nesneyi pitch/yaw/roll veya sabit rotasyona ayarlar.

## Kullanım

```python
controller.step(action="RotateHeldObject", pitch=90, yaw=25, roll=45)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `pitch` | float | Hayır | 0 | Pitch artışı (derece). |
| `yaw` | float | Hayır | 0 | Yaw artışı (derece). |
| `roll` | float | Hayır | 0 | Roll artışı (derece). |
| `rotation` | dict | Hayır | None | Sabit rotasyon {x,y,z} (alternatif). |

## Ön Koşullar

- Ajan nesne tutuyor.

## Etkiler

- Tutulan nesne rotasyonu güncellenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/RotateHeldObject.md`](../pddl_mappings/RotateHeldObject.md)
