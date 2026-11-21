# AddThirdPartyCamera → PDDL Eşlemesi

**AI2-THOR Aksiyonu:** `AddThirdPartyCamera`  
**PDDL Aksiyonu:** `add-third-party-camera`  
**Kategori:** Kamera

## PDDL Tanımı

```pddl
(:action add-third-party-camera
  :parameters (?c - camera)
  
  :effect (and
    (camera-active ?c))
)
```

## AI2-THOR Ön Koşulları → PDDL Predikatları

_Yok._

## AI2-THOR Etkileri → PDDL Etkileri

- Yeni kamera eklenir.
- third_party_camera_frames erişilebilir.


## PDDL Ön Koşulları

_Ön koşul yok (sorgu veya kurulum aksiyonu)._

## PDDL Etkileri

- (camera-active ?c)


## İlgili API Dokümantasyonu

→ [`ai2thor_api/AddThirdPartyCamera.md`](../ai2thor_api/AddThirdPartyCamera.md)
