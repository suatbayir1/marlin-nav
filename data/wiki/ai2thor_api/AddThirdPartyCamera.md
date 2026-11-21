# AddThirdPartyCamera

**Kategori:** Kamera  
**Kaynak:** `raw/metadata.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Sahneye üçüncü parti kamera ekler.

## Kullanım

```python
event = controller.step(action="AddThirdPartyCamera", position=dict(x=-1.25,y=1,z=-1), rotation=dict(x=90,y=0,z=0), fieldOfView=90)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `position` | dict | Evet | - | Global pozisyon. |
| `rotation` | dict | Evet | - | Global rotasyon. |
| `fieldOfView` | int | Hayır | 90 | Görüş alanı (derece). |

## Ön Koşullar

_Yok._

## Etkiler

- Yeni kamera eklenir.
- third_party_camera_frames erişilebilir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/AddThirdPartyCamera.md`](../pddl_mappings/AddThirdPartyCamera.md)
