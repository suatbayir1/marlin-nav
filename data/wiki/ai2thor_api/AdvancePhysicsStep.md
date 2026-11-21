# AdvancePhysicsStep

**Kategori:** Fizik Simülasyonu  
**Kaynak:** `raw/initialization.md`  
**Sorgu Aksiyonu:** Hayır

## Açıklama

Fizik simülasyonunu belirtilen süre ilerletir.

## Kullanım

```python
controller.step(action="AdvancePhysicsStep", timeStep=0.01)
```

## Parametreler

| Parametre | Tip | Zorunlu | Varsayılan | Açıklama |
|-----------|-----|---------|------------|----------|
| `timeStep` | float | Evet | - | Simülasyon süresi (0, 0.05] saniye. |

## Ön Koşullar

- PausePhysicsAutoSim çağrılmış olmalı.

## Etkiler

- Fizik durumu timeStep kadar ilerler.


## İlgili PDDL Eşlemesi

→ [`pddl_mappings/AdvancePhysicsStep.md`](../pddl_mappings/AdvancePhysicsStep.md)
