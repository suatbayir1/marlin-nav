# SetGlobalRoomTempDecayTime

**Kategori:** Sahne Kurulumu  
**Kaynak:** `raw/set_object_states.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Tüm nesneler için global sıcaklık decay süresini ayarlar.

## Kullanım

```python
controller.step(action="SetGlobalRoomTempDecayTime", TimeUntilRoomTemp=20.0)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `TimeUntilRoomTemp` | float | Evet | - | Saniye cinsinden süre. |

## Ön Koşullar

_Yok._

## Etkiler

- Global decay süresi güncellenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/SetGlobalRoomTempDecayTime.md`](../pddl_mappings/SetGlobalRoomTempDecayTime.md)
