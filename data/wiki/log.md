# Wiki Değişiklik Günlüğü

## 2026-06-22 — İlk Oluşturma

### Yapılan İşlemler

1. `/raw/` klasöründeki 11 markdown dosyası incelendi.
2. AI2-THOR `controller.step()` aksiyonları filtrelendi.
3. **64** aksiyon için `/wiki/ai2thor_api/` altında ayrı `.md` dosyaları oluşturuldu.
4. Her aksiyon için `/wiki/pddl_mappings/` altında PDDL eşleme dosyaları tasarlandı.
5. `/wiki/pddl_mappings/domain.md` PDDL domain özeti eklendi.
6. `/wiki/index.md` ve `/wiki/log.md` oluşturuldu.

### Kaynak Dosyalar

| Raw Dosya | İçerik |
|-----------|--------|
| `navigation.md` | Navigasyon aksiyonları |
| `interactive.md` | Manipülasyon ve fizik etkileşimleri |
| `object_state_changes.md` | Nesne durumu değişiklikleri |
| `set_object_states.md` | Sahne kurulum aksiyonları |
| `initialization.md` | Fizik simülasyon kontrolü |
| `domain.md` | Domain randomizasyonu |
| `metadata.md` | Ortam sorguları ve kamera |
| `concepts.md` | Temel kavramlar (aksiyon değil) |
| `installation.md` | Kurulum (aksiyon değil) |
| `scenes.md` | Sahne listesi (aksiyon değil) |
| `object_types.md` | Nesne tipleri (aksiyon değil) |

### Kategori Dağılımı

- **Kamera:** 2 aksiyon
- **Domain Randomizasyonu:** 4 aksiyon
- **Etkileşim / Manipülasyon:** 17 aksiyon
- **Navigasyon:** 13 aksiyon
- **Nesne Durumu Değişiklikleri:** 12 aksiyon
- **Fizik Simülasyonu:** 3 aksiyon
- **Ortam Sorguları:** 5 aksiyon
- **Sahne Kurulumu:** 8 aksiyon

### Üretim

- Betik: `scripts/generate_wiki.py`
- Toplam dosya: 130 (API + PDDL + index + domain)
