# PushObject

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

DirectionalPush'un pushAngle=0 sözdizimsel kısayolu.

## Kullanım

```python
controller.step(action="PushObject", objectId="Mug|0.25|-0.27", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `moveMagnitude` | float | Evet | - | İtme kuvveti. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtını yok sayar. |

## Ön Koşullar

- Nesne pickupable veya moveable.

## Etkiler

- Nesne ileri itilir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/PushObject.md`](../pddl_mappings/PushObject.md)
