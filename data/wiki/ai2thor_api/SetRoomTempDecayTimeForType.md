# SetRoomTempDecayTimeForType

**Kategori:** Sahne Kurulumu  
**Kaynak:** `raw/set_object_states.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Belirli objectType için oda sıcaklığına dönüş süresini ayarlar.

## Kullanım

```python
controller.step(action="SetRoomTempDecayTimeForType", objectType="Bread", TimeUntilRoomTemp=20.0)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectType` | str | Hayır | None | Nesne tipi. |
| `TimeUntilRoomTemp` | float | Evet | - | Saniye cinsinden süre. |

## Ön Koşullar

_Yok._

## Etkiler

- Tip bazlı sıcaklık decay süresi güncellenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/SetRoomTempDecayTimeForType.md`](../pddl_mappings/SetRoomTempDecayTimeForType.md)
