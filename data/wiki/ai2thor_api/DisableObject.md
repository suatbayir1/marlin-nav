# DisableObject

**Kategori:** Sahne Kurulumu  
**Kaynak:** `raw/set_object_states.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Nesneyi görünmez yapar (geçici, EnableObject ile geri alınabilir).

## Kullanım

```python
controller.step(action="DisableObject", objectId="DiningTable|+1.0|+1.0|+1.0")
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | str | Evet | - | Hedef nesne. |

## Ön Koşullar

- Nesne aktif.

## Etkiler

- Nesne devre dışı.
- Destekleyici nesne ise üstündekiler düşebilir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/DisableObject.md`](../pddl_mappings/DisableObject.md)
