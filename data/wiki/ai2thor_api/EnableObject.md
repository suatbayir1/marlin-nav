# EnableObject

**Kategori:** Sahne Kurulumu  
**Kaynak:** `raw/set_object_states.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Devre dışı bırakılmış nesneyi tekrar aktif eder.

## Kullanım

```python
controller.step(action="EnableObject", objectId="DiningTable|+1.0|+1.0|+1.0")
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | str | Evet | - | Hedef nesne. |

## Ön Koşullar

- Nesne disabled durumda.

## Etkiler

- Nesne tekrar görünür.
- Orijinal konumuna döner.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/EnableObject.md`](../pddl_mappings/EnableObject.md)
