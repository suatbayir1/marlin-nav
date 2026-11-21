# DirectionalPush

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Nesneyi belirtilen açıda iter. pickupable veya moveable nesneler için.

## Kullanım

```python
controller.step(action="DirectionalPush", objectId="Sofa|3|2|1", moveMagnitude=100, pushAngle=90)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `moveMagnitude` | float | Evet | - | İtme kuvveti (newton). |
| `pushAngle` | float | Evet | - | İtme yönü [0:360], 0=ileri. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtını yok sayar. |

## Ön Koşullar

- Nesne pickupable veya moveable.
- Görünür/erişilebilir.

## Etkiler

- Nesne hareket eder.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/DirectionalPush.md`](../pddl_mappings/DirectionalPush.md)
