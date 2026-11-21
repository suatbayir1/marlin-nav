# RandomizeMaterials

**Kategori:** Domain Randomizasyonu  
**Kaynak:** `raw/domain.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Sahnedeki tüm malzemeleri rastgele değiştirir.

## Kullanım

```python
controller.step(action="RandomizeMaterials", useTrainMaterials=None, useValMaterials=None, useTestMaterials=None, inRoomTypes=None)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `useTrainMaterials` | Optional[bool] | Hayır | None | Eğitim malzemeleri. |
| `useValMaterials` | Optional[bool] | Hayır | None | Validasyon malzemeleri. |
| `useTestMaterials` | Optional[bool] | Hayır | None | Test malzemeleri. |
| `inRoomTypes` | List[str] | Hayır | None | Oda tipleri filtresi. |

## Ön Koşullar

_Yok._

## Etkiler

- Malzemeler rastgelelenir.
- Reset ile eski haline döner.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/RandomizeMaterials.md`](../pddl_mappings/RandomizeMaterials.md)
