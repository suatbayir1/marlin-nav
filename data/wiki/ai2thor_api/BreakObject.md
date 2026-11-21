# BreakObject

**Kategori:** Nesne Durumu Değişiklikleri  
**Kaynak:** `raw/object_state_changes.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Kırılabilir nesneyi kırar (geri alınamaz, reset gerekir).

## Kullanım

```python
controller.step(action="BreakObject", objectId="Vase|0.25|0.27|-0.95", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef nesne. |
| `forceAction` | bool | Hayır | False | Mesafe kısıtı. |

## Ön Koşullar

- breakable=True.
- Görünür/erişilebilir.

## Etkiler

- isBroken=True


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/BreakObject.md`](../pddl_mappings/BreakObject.md)
