# RemoveFromScene

**Kategori:** Sahne Kurulumu  
**Kaynak:** `raw/set_object_states.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Nesneyi sahneden kalıcı olarak kaldırır.

## Kullanım

```python
controller.step(action="RemoveFromScene", objectId="Mug|+0.25|-0.27|+1.05")
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `objectId` | str | Evet | - | Hedef nesne. |

## Ön Koşullar

- Nesne sahnede mevcut.

## Etkiler

- Nesne yok edilir (reset gerekir).


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/RemoveFromScene.md`](../pddl_mappings/RemoveFromScene.md)
