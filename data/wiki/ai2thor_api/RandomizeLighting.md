# RandomizeLighting

**Kategori:** Domain Randomizasyonu  
**Kaynak:** `raw/domain.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Sahne aydınlatmasını rastgele değiştirir.

## Kullanım

```python
controller.step(action="RandomizeLighting", brightness=(0.5, 1.5), randomizeColor=True, hue=(0, 1), saturation=(0.5, 1), synchronized=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `brightness` | Tuple[float,float] | Hayır | (0.5, 1.5) | Parlaklık aralığı. |
| `randomizeColor` | bool | Hayır | True | Renk rastgeleleme. |
| `hue` | Tuple[float,float] | Hayır | (0, 1) | Renk tonu aralığı. |
| `saturation` | Tuple[float,float] | Hayır | (0.5, 1) | Doygunluk aralığı. |
| `synchronized` | bool | Hayır | False | Tüm ışıklar senkron. |

## Ön Koşullar

_Yok._

## Etkiler

- Aydınlatma rastgelelenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/RandomizeLighting.md`](../pddl_mappings/RandomizeLighting.md)
