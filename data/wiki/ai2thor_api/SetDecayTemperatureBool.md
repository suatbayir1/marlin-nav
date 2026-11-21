# SetDecayTemperatureBool

**Kategori:** Sahne Kurulumu  
**Kaynak:** `raw/set_object_states.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Sıcaklık decay mekanizmasını açar/kapatır.

## Kullanım

```python
controller.step(action='SetDecayTemperatureBool', allowDecayTemperature=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `allowDecayTemperature` | bool | Hayır | True | Decay izni. |

## Ön Koşullar

_Yok._

## Etkiler

- Sıcaklık decay davranışı değişir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/SetDecayTemperatureBool.md`](../pddl_mappings/SetDecayTemperatureBool.md)
