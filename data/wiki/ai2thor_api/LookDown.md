# LookDown

**Kategori:** Navigasyon  
**Kaynak:** `raw/navigation.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Kameranın pitch açısını aşağı artırır.

## Kullanım

```python
controller.step("LookDown")
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `degrees` | float | Hayır | 30 | Aşağı bakış açısı (>0). |

## Ön Koşullar

- horizon > -30 olmalı.

## Etkiler

- cameraHorizon artar (aşağı bakış).


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/LookDown.md`](../pddl_mappings/LookDown.md)
