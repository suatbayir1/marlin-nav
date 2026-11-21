# PullObject

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

DirectionalPush'un pushAngle=180 sözdizimsel kısayolu.

## Kullanım

```python
controller.step(action="PullObject", objectId="Mug|0.25|-0.27", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `moveMagnitude` | float | Evet | - | Çekme kuvveti. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtını yok sayar. |

## Ön Koşullar

- Nesne pickupable veya moveable.

## Etkiler

- Nesne geri çekilir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/PullObject.md`](../pddl_mappings/PullObject.md)
