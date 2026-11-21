# GetObjectInFrame

**Kategori:** Ortam Sorguları  
**Kaynak:** `raw/metadata.md`  
**Sorgu Aksiyonu:** Evet

## Açıklama

Ekran koordinatındaki nesnenin objectId'sini döndürür.

> **Not:** Bu bir sorgu aksiyonudur; ortam durumunu değiştirmez.

## Kullanım

```python
query = controller.step(action="GetObjectInFrame", x=0.64, y=0.40, checkVisible=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `x` | float | Evet | - | Ekran x [0:1]. |
| `y` | float | Evet | - | Ekran y [0:1]. |
| `checkVisible` | bool | Hayır | False | visibilityDistance kontrolü. |

## Ön Koşullar

_Yok._

## Etkiler

- actionReturn: objectId veya None.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/GetObjectInFrame.md`](../pddl_mappings/GetObjectInFrame.md)
