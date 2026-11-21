# UpdateThirdPartyCamera

**Kategori:** Kamera  
**Kaynak:** `raw/metadata.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Mevcut üçüncü parti kameranın durumunu günceller.

## Kullanım

```python
controller.step(action="UpdateThirdPartyCamera", thirdPartyCameraId=0, position=dict(x=-1.25,y=1,z=-1))
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `thirdPartyCameraId` | int | Evet | - | Kamera indeksi. |
| `position` | dict | Hayır | None | Yeni pozisyon. |
| `rotation` | dict | Hayır | None | Yeni rotasyon. |
| `fieldOfView` | int | Hayır | None | Yeni FOV. |

## Ön Koşullar

- Kamera mevcut olmalı.

## Etkiler

- Kamera parametreleri güncellenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/UpdateThirdPartyCamera.md`](../pddl_mappings/UpdateThirdPartyCamera.md)
