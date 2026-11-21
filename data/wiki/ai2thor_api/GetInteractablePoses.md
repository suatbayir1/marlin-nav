# GetInteractablePoses

**Kategori:** Ortam Sorguları  
**Kaynak:** `raw/metadata.md`  
**Sorgu Aksiyonu:** Evet

## Açıklama

Bir nesneyle etkileşim kurulabilecek tüm ajan pozlarını döndürür.

> **Not:** Bu bir sorgu aksiyonudur; ortam durumunu değiştirmez.

## Kullanım

```python
event = controller.step(action="GetInteractablePoses", objectId="Apple|-1.0|+1.0|+1.5")
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `positions` | list | Hayır | None | Aranacak pozisyonlar. |
| `rotations` | list | Hayır | None | Aranacak rotasyonlar. |
| `horizons` | list | Hayır | None | Aranacak horizon değerleri. |
| `standings` | list | Hayır | None | Ayakta/çömelmiş durumları. |

## Ön Koşullar

_Yok._

## Etkiler

- actionReturn: etkileşimli poz listesi.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/GetInteractablePoses.md`](../pddl_mappings/GetInteractablePoses.md)
