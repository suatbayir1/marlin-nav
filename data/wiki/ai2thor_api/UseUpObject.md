# UseUpObject

**Kategori:** Nesne Durumu Değişiklikleri  
**Kaynak:** `raw/object_state_changes.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Tüketilebilir nesnenin bir kısmını kullanır (tuvalet kağıdı vb.).

## Kullanım

```python
controller.step(action="UseUpObject", objectId="ToiletPaper|0.25|-0.27|0.95", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtı. |

## Ön Koşullar

- canBeUsedUp=True.
- Tükenmemiş olmalı.

## Etkiler

- isUsedUp=True (veya kısmi tüketim).


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/UseUpObject.md`](../pddl_mappings/UseUpObject.md)
