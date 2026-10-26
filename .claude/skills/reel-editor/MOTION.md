# Movimiento

Reglas destiladas de los skills de motion design más usados con Opus 5.5 (claude-remotion-skill, aiidelist, nopefallacy). Son el mínimo para que no parezca una plantilla.

## Reglas

1. **Nunca interpolación lineal.** `spring()` con los presets de `theme.springs`, o `interpolate` con `theme.easings` y `extrapolate…: "clamp"`.
2. **Las entradas animan 2–3 propiedades a la vez** (opacidad + posición + desenfoque o escala). Una sola propiedad parece barata.
3. **Escalonar siempre.** Palabras, líneas y elementos de una tarjeta entran con 2–4 fotogramas de desfase.
4. **Las salidas existen y son más rápidas que las entradas** (~0,5×). Nada desaparece de golpe salvo en un corte.
5. **Lo que está en reposo respira.** Micro-movimiento senoidal (escala ±1 %, deriva de pocos px). Nada totalmente congelado.
6. **Todo el timing sale de `fps`** (`seconds * fps`) o de los fotogramas de `cut_transcript.md`. Sin números mágicos.
7. **Un solo `theme.ts`.** Sin colores, fuentes ni easings en línea.
8. **Quietud antes de una revelación**: 300–600 ms sin movimiento antes del momento fuerte.
9. **Rebote solo en el momento héroe** (`springs.hero`), uno por beat como mucho. El resto, `snappy` o `smooth`.
10. **Determinista.** Sin `Math.random()`; si hace falta ruido, `random(seed)` de Remotion.
11. **Sincronía con la voz.** Un elemento entra en el fotograma en que se dice su palabra (o 2–3 fotogramas antes), nunca después.
12. **Legibilidad.** Un titular se lee al menos 1,2 s quieto antes de salir.

## Herramientas disponibles en `@remotion/effects` (4.0.538)

Se aplican con la prop `effects` de `<Video>` (ver `remotion-best-practices` → `remotion-markup/effects.md`).

- **Color:** `colorCorrection`, `lut` (.cube), `levels`, `whiteBalance`, `grayscale` (para B/N → color), `duotone`, `tint`.
- **Transiciones y énfasis:** `zoom-blur`, `light-leak`, `chromatic-aberration`, `lens-blur`, `radial-progressive-blur`, `glow`, `shine`.
- **Textura:** `noise`, `vignette`, `paper`, `halftone`.
- Transiciones entre escenas: `@remotion/transitions` (`TransitionSeries`).

## Rendimiento

- `<Video>` de `@remotion/media` para el metraje (sale de `lib/Footage`).
- Los efectos WebGL cuestan en cada fotograma: aplícalos solo durante el tramo que los necesita (dentro de una `Sequence`).
- Comprueba con stills a mitad de escala antes de cualquier render completo.
