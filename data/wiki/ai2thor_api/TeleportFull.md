# TeleportFull

**Kategori:** Navigasyon  
**Kaynak:** `raw/navigation.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Teleport'un katı versiyonu; tüm serbestlik dereceleri zorunludur.

## Kullanım

```python
controller.step(action="TeleportFull", position=dict(x=1,y=0.9,z=-1.5), rotation=dict(x=0,y=270,z=0), horizon=30, standing=True)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `position` | dict | Evet | - | Global pozisyon (zorunlu). |
| `rotation` | dict | Evet | - | Gövde rotasyonu (zorunlu). |
| `horizon` | float | Evet | - | Kamera horizon (zorunlu). |
| `standing` | bool | Evet | - | Duruş durumu (zorunlu). |

## Ön Koşullar

- Tüm parametreler geçerli olmalı.

## Etkiler

- Ajan pozu tam olarak ayarlanır.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/TeleportFull.md`](../pddl_mappings/TeleportFull.md)
