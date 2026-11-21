# GetSpawnCoordinatesAboveReceptacle

**Kategori:** Ortam Sorguları  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Evet

## Açıklama

Receptacle üzerindeki geçerli spawn koordinatlarını döndürür.

> **Not:** Bu bir sorgu aksiyonudur; ortam durumunu değiştirmez.

## Kullanım

```python
controller.step(action="GetSpawnCoordinatesAboveReceptacle", objectId="CounterTop|1|1|1", anywhere=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef receptacle. |
| `anywhere` | bool | Hayır | False | Görüş dışı koordinatları da döndür. |

## Ön Koşullar

_Yok._

## Etkiler

- actionReturn: xyz koordinat listesi.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/GetSpawnCoordinatesAboveReceptacle.md`](../pddl_mappings/GetSpawnCoordinatesAboveReceptacle.md)
