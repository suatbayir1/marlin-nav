# RotateRight

**Kategori:** Navigasyon  
**Kaynak:** `raw/navigation.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Ajanın gövde yaw rotasyonunu sağa çevirir.

## Kullanım

```python
controller.step(action="RotateRight", degrees=None)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `degrees` | Optional[float] | Hayır | None | rotateStepDegrees varsayılanını geçersiz kılar. |

## Ön Koşullar

_Yok._

## Etkiler

- Ajan rotasyonu güncellenir.
- Tutulan nesne rotasyonu sıfırlanır.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/RotateRight.md`](../pddl_mappings/RotateRight.md)
