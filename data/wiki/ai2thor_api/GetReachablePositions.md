# GetReachablePositions

**Kategori:** Ortam Sorguları  
**Kaynak:** `raw/metadata.md`  
**Sorgu Aksiyonu:** Evet

## Açıklama

Ajanın ulaşabileceği tüm grid pozisyonlarını BFS ile döndürür. Ortam durumunu değiştirmez.

> **Not:** Bu bir sorgu aksiyonudur; ortam durumunu değiştirmez.

## Kullanım

```python
positions = controller.step(action="GetReachablePositions").metadata["actionReturn"]
```

## Parametreler

_Parametre yok._

## Ön Koşullar

_Yok._

## Etkiler

- actionReturn: ulaşılabilir pozisyon listesi.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/GetReachablePositions.md`](../pddl_mappings/GetReachablePositions.md)
