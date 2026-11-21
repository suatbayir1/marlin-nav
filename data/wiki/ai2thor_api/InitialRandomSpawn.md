# InitialRandomSpawn

**Kategori:** Domain Randomizasyonu  
**Kaynak:** `raw/domain.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Pickupable nesnelerin pozisyonlarını rastgele yerleştirir.

## Kullanım

```python
controller.step(action="InitialRandomSpawn", randomSeed=0, forceVisible=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `randomSeed` | int | Hayır | 0 | Rastgelelik tohumu. |
| `forceVisible` | bool | Hayır | False | Görünür alana zorla. |
| `numPlacementAttempts` | int | Hayır | 5 | Yerleştirme deneme sayısı. |
| `placeStationary` | bool | Hayır | True | Deterministik yerleşim. |
| `numDuplicatesOfType` | list | Hayır | [] | Tip bazlı kopya sayısı. |
| `excludedReceptacles` | list | Hayır | [] | Hariç tutulan receptacle'lar. |
| `excludedObjectIds` | list | Hayır | [] | Hariç tutulan nesneler. |

## Ön Koşullar

- Sahne reset edilmiş olmalı (seed doğruluğu için).

## Etkiler

- Nesne pozisyonları değişir.
- objectId'ler yeniden hesaplanır.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/InitialRandomSpawn.md`](../pddl_mappings/InitialRandomSpawn.md)
