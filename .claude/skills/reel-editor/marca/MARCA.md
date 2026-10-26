# Marca EnsoMovers para reels

Destilado del manual de identidad visual (rebranding 2026). Este archivo y esta carpeta sustituyen al manual en el día a día: no hace falta volver al manual salvo cambio de identidad.

Esta carpeta se enlaza en cada reel como `public/marca`, así que sus archivos se usan con `staticFile("marca/…")`.

## Principio rector

> Si un elemento visual no comunica nada, se elimina.

- **Referentes:** arquitectura japonesa contemporánea, editorial científica (Nature, Scientific American), diseño escandinavo, wabi-sabi.
- **Valores:** minimalismo honesto, claridad, toque humano y natural. Ni lujo ni aspiracional: profesionalidad, confianza y cercanía.

| Evocar | Evitar |
|---|---|
| Claridad | Frialdad clínica |
| Profesionalidad | Corporativismo |
| Naturalidad | Hippie / espiritual |
| Calma | Pasividad |
| Rigor | Rigidez |
| Cercanía | Informalidad descuidada |

## Color: Luminous Enso Pure

| Nombre | Hex | Rol | Proporción |
|---|---|---|---|
| Negro | `#0A0A0A` | Texto, fondos oscuros, encabezados | base |
| Blanco | `#FFFFFF` | Fondos, texto sobre oscuro | base |
| Mist | `#E5E8E4` | Fondos suaves, separadores, tarjetas | 15 % |
| Sage | `#A2B598` | **Acento principal** | 10 % |
| Earth | `#8C7565` | Detalles | 5 % |

Tonos de apoyo de las plantillas: sage claro `#D4DECE`, earth claro `#B8A99D`.

**Combinaciones:**
- Sobre fondo claro: texto negro, acentos en sage o earth.
- Sobre fondo oscuro: texto blanco, acento en sage.
- Todo texto cumple WCAG AA como mínimo.

**Nunca:** sage como fondo principal, marrón como color de texto, gris como acento.

**En vídeo** (decisión del usuario, 2026-10-25): el texto sobre el metraje va siempre en **blanco con sombra amplia** y la palabra clave en **sage**, también sobre paredes claras; el usuario prioriza esa estética sobre el contraste AA estricto. Las tarjetas son blanco roto (`#F8F9F7`) con texto negro y marcador sage. El earth queda para detalles gráficos (metadatos, insignia ✕), nunca para texto corrido.

## Tipografía

| Uso en el reel | Fuente | Archivo en `fuentes/` |
|---|---|---|
| Títulos grandes | **Satoshi Bold 700, MAYÚSCULAS** | `Satoshi-Variable.ttf` |
| Subtítulos de sección, rótulos | Satoshi Regular 400 | `Satoshi-Variable.ttf` |
| Subtítulo hablado (captions) | Fira Sans Bold 700, blanco con sombra | `FiraSans-Bold.ttf` |
| Palabra de contraste en un título | Fira Sans Light Italic 300 | `FiraSans-LightItalic.ttf` |
| Texto de tarjetas, explicaciones | Fira Sans Light 300 | `FiraSans-Light.ttf` |
| Conceptos clave, CTA | Fira Sans Bold 700 | `FiraSans-Bold.ttf` |
| Datos, métricas, ángulos, repeticiones, tiempos | JetBrains Mono 400, en sage | `JetBrainsMono-Variable.ttf` |

"Satoshi estructura la marca. Fira Sans sostiene la lectura." JetBrains Mono es lo que da el aire de editorial científica: úsalo para cualquier dato medible (`90°`, `3 × 30 s`, `2 semanas`).

Licencias: Fira Sans y JetBrains Mono (OFL) van en el repositorio. **Satoshi no**: su licencia (Fontshare EULA, `Satoshi-LICENSE.txt`) prohíbe redistribuirla, así que cada equipo la descarga gratis de Fontshare durante la instalación (`INSTALAR.md`) y queda fuera de git.

## Logo

- El ensō solo: `logo/enso-negro.png` y `logo/enso-blanco.png` (transparentes, recortados, 800 px).
- Con nombre: ensō + "ENSO MOVERS" en Satoshi mayúsculas con tracking amplio (~0,2 em) debajo.
- El logo antiguo de pincel con texto (`Logo Enso Movers.JPG`) ya no se usa.
- Para YouTube el manual pide intro/outro con una animación simple del ensō. En reels, como mucho una aparición breve, normalmente al cierre.

## Instagram y fotografía

- **Feed:** predominio de negro, blanco y sage. **Reels minimalistas, sin transiciones excesivas.**
- **Buscamos:** luz natural cálida y suave, fondos limpios, el cuerpo en movimiento (gesto, posición, técnica), expresiones reales.
- **Evitamos:** stock genérico, luz dura con neón, el cuerpo como objeto estético (no somos fitness convencional), filtros agresivos tipo "mood", imágenes sobrecargadas de texto.
