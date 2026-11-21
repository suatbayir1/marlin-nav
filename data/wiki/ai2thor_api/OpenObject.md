# OpenObject

**Kategori:** Nesne Durumu Değişiklikleri  
**Kaynak:** `raw/object_state_changes.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Açılabilir nesneyi belirtilen openness oranına açar.

## Kullanım

```python
controller.step(action="OpenObject", objectId="Book|0.25|-0.27|0.95", openness=1, forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `openness` | float | Hayır | 1 | Açıklık oranı [0:1]. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtını yok sayar. |

## Ön Koşullar

- openable=True.
- Görünür/erişilebilir.
- Çarpışma engeli yok.

## Etkiler

- openness güncellenir.
- isOpen=True (openness>0).


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/OpenObject.md`](../pddl_mappings/OpenObject.md)
