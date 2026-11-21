# Teleport

**Kategori:** Navigasyon  
**Kaynak:** `raw/navigation.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Ajanın pozunu tek adımda belirtilen konuma ayarlar. Belirtilmeyen DOF'lar korunur.

## Kullanım

```python
controller.step(action="Teleport", position=dict(x=1,y=0.9,z=-1.5), rotation=dict(x=0,y=270,z=0), horizon=30, standing=True)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `position` | dict | Hayır | None | Global (x,y,z) pozisyon. |
| `rotation` | dict | Hayır | None | Gövde yaw rotasyonu. |
| `horizon` | float | Hayır | None | Kamera pitch ([-30, 60]). |
| `standing` | bool | Hayır | None | Ayakta/çömelmiş durumu. |

## Ön Koşullar

- Hedef poz geçerli olmalı (duvar/çarpışma yok).

## Etkiler

- Ajan pozu güncellenir.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/Teleport.md`](../pddl_mappings/Teleport.md)
