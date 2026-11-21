# LookUp

**Kategori:** Navigasyon  
**Kaynak:** `raw/navigation.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Kameranın pitch açısını yukarı artırır ([-30, 60] aralığında sınırlı).

## Kullanım

```python
controller.step(action="LookUp", degrees=30)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `degrees` | float | Hayır | 30 | Yukarı bakış açısı (>0). |

## Ön Koşullar

- horizon < 60 olmalı.

## Etkiler

- cameraHorizon azalır (yukarı bakış).


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/LookUp.md`](../pddl_mappings/LookUp.md)
