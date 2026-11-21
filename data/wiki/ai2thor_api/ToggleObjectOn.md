# ToggleObjectOn

**Kategori:** Nesne Durumu Değişiklikleri  
**Kaynak:** `raw/object_state_changes.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Toggleable nesneyi açık (on) durumuna getirir.

## Kullanım

```python
controller.step(action="ToggleObjectOn", objectId="LightSwitch|0.25|-0.27|0.95", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtı. |

## Ön Koşullar

- toggleable=True.
- Kapalı olmalı.
- Görünür/erişilebilir.

## Etkiler

- isToggled=True


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/ToggleObjectOn.md`](../pddl_mappings/ToggleObjectOn.md)
