# GetCoordinateFromRaycast

**Kategori:** Ortam Sorguları  
**Kaynak:** `raw/metadata.md`  
**Sorgu Aksiyonu:** Evet

## Açıklama

Ekran koordinatından ışın göndererek çarpışma noktasının dünya koordinatını döndürür.

> **Not:** Bu bir sorgu aksiyonudur; ortam durumunu değiştirmez.

## Kullanım

```python
query = controller.step(action="GetCoordinateFromRaycast", x=0.64, y=0.40)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `x` | float | Evet | - | Ekran x [0:1]. |
| `y` | float | Evet | - | Ekran y [0:1]. |

## Ön Koşullar

_Yok._

## Etkiler

- actionReturn: (x,y,z) koordinat.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/GetCoordinateFromRaycast.md`](../pddl_mappings/GetCoordinateFromRaycast.md)
