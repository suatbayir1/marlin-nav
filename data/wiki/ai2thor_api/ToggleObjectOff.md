# ToggleObjectOff

**Kategori:** Nesne Durumu Değişiklikleri  
**Kaynak:** `raw/object_state_changes.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Toggleable nesneyi kapalı (off) durumuna getirir.

## Kullanım

```python
controller.step(action="ToggleObjectOff", objectId="LightSwitch|0.25|-0.27|0.95", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtı. |

## Ön Koşullar

- toggleable=True.
- Açık olmalı.

## Etkiler

- isToggled=False


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/ToggleObjectOff.md`](../pddl_mappings/ToggleObjectOff.md)
