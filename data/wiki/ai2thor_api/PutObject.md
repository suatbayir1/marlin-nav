# PutObject

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Tutulan nesneyi hedef receptacle üzerine/ içine yerleştirir.

## Kullanım

```python
controller.step(action="PutObject", objectId="CounterTop|1|1|1", forceAction=False, placeStationary=True)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | string | Evet | - | Hedef receptacle objectId. |
| `forceAction` | bool | Hayır | False | Receptacle kısıtlarını yok sayar. |
| `placeStationary` | bool | Hayır | True | True=deterministik yerleşim. |

## Ön Koşullar

- Ajan nesne tutuyor.
- Hedef receptacle=True.
- Geçerli receptacle kısıtları.

## Etkiler

- Nesne receptacle'a yerleşir.
- isPickedUp=False


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/PutObject.md`](../pddl_mappings/PutObject.md)
