# DropHandObject

**Kategori:** Etkileşim / Manipülasyon  
**Kaynak:** `raw/interactive.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Tutulan nesneyi bırakır; fizik motoru iniş noktasını belirler.

## Kullanım

```python
controller.step(action="DropHandObject", forceAction=False)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `forceAction` | bool | Hayır | False | Çarpışma olsa bile bırakır. |

## Ön Koşullar

- Ajan nesne tutuyor.
- Çarpışma engeli yok (forceAction=False).

## Etkiler

- Nesne serbest bırakılır.
- isPickedUp=False


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/DropHandObject.md`](../pddl_mappings/DropHandObject.md)
