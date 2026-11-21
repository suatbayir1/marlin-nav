# PickupObject

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Belirtilen pickupable nesneyi ajanın eline alır.

## Kullanım

```python
controller.step(action="PickupObject", objectId="Apple|1|1|1", forceAction=False, manualInteract=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesnenin objectId'si. |
| `forceAction` | bool | Hayır | False | visibilityDistance kısıtını yok sayar. |
| `manualInteract` | bool | Hayır | False | True ise nesne elde teleport olmaz. |

## Ön Koşullar

- Nesne pickupable=True.
- Ajan eli boş.
- Nesne görünür/erişilebilir.
- Çarpışma yok.

## Etkiler

- isPickedUp=True
- İçerdiği nesneler de birlikte alınabilir (receptacle).


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/PickupObject.md`](../pddl_mappings/PickupObject.md)
