# ThrowObject

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Tutulan nesneyi ileri yönde belirtilen kuvvetle fırlatır.

## Kullanım

```python
controller.step(action="ThrowObject", moveMagnitude=150.0, forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `moveMagnitude` | float | Evet | - | Fırlatma kuvveti (newton). |
| `forceAction` | bool | Hayır | False | Çarpışma kısıtını yok sayar. |

## Ön Koşullar

- Ajan nesne tutuyor.

## Etkiler

- Nesne fırlatılır.
- isPickedUp=False


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/ThrowObject.md`](../pddl_mappings/ThrowObject.md)
