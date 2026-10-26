# Efectos de sonido

Biblioteca compartida por todos los reels. En código se usa con `<Sfx name=… at={frame} />` de `lib/Sfx.tsx`, que lleva el mismo catálogo con nombres cortos: al añadir un sonido, añádelo en los dos sitios.
Criterio de marca: pocos, suaves, orgánicos. Cada efecto acompaña algo que se ve.

- **Ataque:** segundos de silencio antes del golpe. Para que suene justo en el fotograma F, el `<Sequence>` del audio empieza en `F − ataque × fps`.
- **Volumen:** valor de partida para la prop `volume` de `<Audio>`, que deja el efecto unos 10–12 dB por debajo de la voz (−14 LUFS).

| Archivo | Uso | Dur. | Ataque | Volumen |
|---|---|---|---|---|
| `dragon-studio-pop-402324 (1).mp3` | Entra una palabra, una tarjeta o un dato | 0,72 s | 0,19 s | 0,3 |
| `dragon-studio-simple-whoosh-382724.mp3` | Cambio de idea, movimiento de cámara o barrido | 0,57 s | 0,07 s | 0,25 |
| `dragon-studio-riser-swoosh-transition-390289.mp3` | Transición con subida corta, revelación | 0,99 s | 0,17 s | 0,3 |
| `dragon-studio-swoosh-riser-reverb-390309.mp3` | Tensión larga antes de una revelación. Recortar con `trimBefore` | 6,19 s | 0,67 s | 0,35 |
| `dragon-studio-flipping-book-page-499646.mp3` | Tarjeta de papel que entra o se gira | 1,22 s | 0,02 s | 0,4 |
| `freesound_community-fast-and-slow-marker-strokes-82047.mp3` | Marcador sage o subrayado. Usar un trazo (~0,4 s) | 4,58 s | 0,06 s | 0,8 |
| `dragon-studio-typing-with-keyboard-435489.mp3` | Dato en JetBrains Mono que se escribe. Recortar a la duración del texto | 5,42 s | 0,04 s | 0,5 |
| `nickpanek-mechanical-keyboard-typing-sound-effect-ai-made-sfx-473872.mp3` | Alternativa de tecleo, más mecánica y fuerte | 6,03 s | 0,53 s | 0,25 |
| `freesound_community-camera-shutter-6305.mp3` | Congelar una postura, foto fija | 0,34 s | 0,04 s | 0,35 |
| `freesound_community-writingpensignaturepaper-102967.mp3` | Trazo de pincel o dibujo a mano sobre el plano (flechas, círculos). Recortar a la duración del trazo | 3,74 s | 0,38 s | 1,0 |
| `nikin-scratch-sound-effect-for-video-title-underline-317747.mp3` | **Subrayado o marcador sage bajo una palabra** (preferido al de rotulador) | 0,84 s | 0,05 s | 0,25 |

No hay golpe grave de impacto; para el gancho, usar el pop o el riser corto.
