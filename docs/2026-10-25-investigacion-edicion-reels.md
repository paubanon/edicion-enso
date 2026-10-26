# Edición de reels con Claude Opus 5.5: investigación destilada

Fecha: 2026-10-25 · Para: EnsoMovers · Estado: borrador para decidir el setup

## 1. Qué hace la gente con Opus 5.5 (y qué no)

**Idea central, en la que coinciden todas las fuentes sobre Opus 5.5:** el modelo no genera píxeles. Escribe un programa (Remotion o HyperFrames) que dibuja cada fotograma, y ffmpeg lo monta. El metraje real (tú hablando, B-roll) se graba, y Claude corta, gradúa, compone gráficos y subtítulos encima.

Fuentes que hablan explícitamente de Opus 5.5:

| Fuente | Lo útil |
|---|---|
| [dsebastien.net](https://www.dsebastien.net/2026-10-04-claude-opus-5-5-ask-for-a-video-get-a-program-you-can-edit/) | Las revisiones se piden en una frase ("Slow down the second scene") y se re-renderiza. El código debe ser legible y pequeño, si no, editar por prompt falla. |
| [bettertoken.ai](https://bettertoken.ai/en/blog/claude-opus-5-5-remotion-video-workflow/) | Flujo `brief.md` → composición Remotion con ID estable → Studio → render CLI → `ffprobe`. Reglas: "frame-based APIs, every frame deterministic", "no claim success unless render exits 0", solo assets locales. |
| [aiidelist.com](https://aiidelist.com/blog/opus-5-5-motion-design) | 7 fases (objetivo → assets reales → storyboard → renderer → fotogramas representativos → revisión de timing → render final). 24 plantillas de prompt, incluida "vertical viral reel" y "render QA con contact sheet". |
| [learnwithseb.com](https://www.learnwithseb.com/blog/claude-opus-5-5-video-editing-cost/) | Coste real: un talking head de 4:23 ≈ 34M tokens de entrada (~20 $ a precio API). Esfuerzo máximo agotó una sesión de 5 h en un vídeo de 15 s. Regla firme: no alterar la voz ni la imagen del presentador. |
| [aiblewmymind](https://aiblewmymind.substack.com/p/claude-opus-5-5-video-animations) | Usó Opus 5.5 en esfuerzo **alto** para todos los vídeos. Sonnet 5.5 cuesta la mitad y sirve para retoques. |
| [Resumen de búsquedas sobre esfuerzo](https://www.orcarouter.ai/blog/claude-opus-5-5-video-plan-one-shot) | Consenso: medio para retoques y re-renders, **xhigh** para piezas nuevas, max solo si los 3 primeros segundos lo justifican. Contact sheet antes del render completo. |
| [clixie.ai](https://www.clixie.ai/blog/claude-code-video-editing) | La calidad del plan cae pasados ~200–260K tokens de sesión: pedir resumen de traspaso y abrir sesión nueva. Un render a la vez (la RAM se dispara). Error de ~120 ms en los bordes de palabra de Whisper. |
| [sergeichyrkov.com](https://sergeichyrkov.com/blog/claude-opus-motion-remotion-threejs) | Dejar que Claude haga preguntas antes de construir. Assets reales, nunca generados, para producto/persona. |

Skills de la comunidad (no atadas a un modelo, pero las usan con Opus 5.5):

| Skill | Qué aporta | Motor |
|---|---|---|
| [browser-use/video-use](https://github.com/browser-use/video-use) (~13K ★) | Cortes guiados por transcripción con timestamps por palabra (ElevenLabs Scribe), `timeline_view` (tira de fotogramas + forma de onda + palabras en PNG) en cada corte, fundidos de audio de 30 ms, etalonaje por segmento, autoevaluación con hasta 3 re-renders. | ffmpeg + cualquier motor de overlays |
| [tenfoldmarc/video-edit-skill](https://github.com/tenfoldmarc/video-edit-skill) | El más cercano a tu estética: **palabras grandes detrás de la cabeza** (quita el fondo), 3 "looks", inserts animados, zona segura de Instagram, revisión fotograma a fotograma de cada corte, punch-ins desde 4K. | HyperFrames + faster-whisper |
| [haidrrrry/claude-remotion-skill](https://github.com/haidrrrry/claude-remotion-skill) | 10 reglas de movimiento y bucle "render → inspeccionar fotogramas → corregir → re-render". | Remotion |
| [nopefallacy/vertical-video-editing-skills](https://github.com/nopefallacy/vertical-video-editing-skills) | "Los fotogramas son páginas diseñadas, no vídeo con texto encima". Estilos como paquetes de tokens (`FRAME.md`). Script de verificación con pass/fail. | HyperFrames |
| [manotsiris (Substack)](https://manotsiris.substack.com/p/the-claude-code-setup-that-edits) | 9 estaciones con storyboard aprobado antes de renderizar, y "guardar cada corrección como regla permanente". Analiza 3 reels de referencia y genera un skill `my-editing-style`. | ffmpeg + HyperFrames |
| Remotion oficial (`remotion-best-practices`, ya instalado) | Reglas de la API de Remotion, captions con `createTikTokStyleCaptions()`, whisper.cpp. | Remotion |
| HyperFrames oficial (`heygen-com/hyperframes`) | ~450 bloques (tipografía cinética, transiciones, captions), `/media-use` con recortes de fondo y looks de color. | HyperFrames |

## 2. Remotion o HyperFrames

| | Remotion | HyperFrames |
|---|---|---|
| Autoría | React/TS, función de `frame` | HTML + GSAP con atributos de tiempo |
| A favor para ti | Ya tienes un proyecto funcionando (`lesion-hombro/edit/reel`) y el skill oficial instalado. Control determinista fotograma a fotograma, más historial y documentación. | La mayoría de skills de reels de talking head de 2026 están construidos sobre él. Recorte de fondo integrado y registro de bloques. |
| En contra | No trae recorte de fondo: hay que generar la máscara aparte. | Rehacer lo que ya tienes. Proyecto más joven. |
| Licencia | Gratis para individuos y empresas de hasta 3 personas. Más grandes pagan. | Apache 2.0 |

**Mi recomendación: Remotion como compositor.** El texto detrás de ti depende de la máscara de la persona, no del motor, y esa máscara se puede generar en local y meter en Remotion como una capa más. Tomo de los skills de HyperFrames las reglas y las ideas de diseño, no el motor.

## 3. Análisis de tus referencias

Contact sheets en el scratchpad de la sesión. Lo que hace cada uno:

**A · `DcbgKLeMcXK` (15 s, "hook one…five")**
- Título fijo: "hook" en sans pesada blanca con número en script itálica amarilla superpuesto.
- **El título queda detrás de lo que hay en escena**: el poste tapa la "o", las personas pasan por delante.
- Efecto de clon/estela de movimiento. Planos fijos con trípode. Viñeta y bajo oscurecido.
- Cierre: listas de interfaz inclinadas en 3D, flotando alrededor de él.

**B · `DdhoUcHuHCH` (17 s, "visual hooks")**
- Tipografía cinética: cada frase con su propia combinación (condensada roja + script, azul, blanca extendida, verde).
- Transición de barrido circular de color. Cambio de B/N a color.
- El texto vive en el tercio superior, encima de la cabeza, nunca sobre la cara.

**C · `DehbdDYssBE` (56 s, editado por Claude)**
- **Paleta sacada de la habitación**: verde profundo de las paredes + crema + el magenta del jersey.
- **Números y palabras serif enormes detrás de la cabeza** ("1 2 3", "ZERO", "1").
- Subtítulo en píldora verde pequeña con palabra activa resaltada, a la altura del pecho.
- Tarjetas de interfaz editoriales en crema y verde (calendario, checklist con tachado, waitlist, comentario, barra de progreso) que ilustran lo que dice.
- Tarjeta de título a pantalla completa. Transición de zoom con desenfoque. Varios ángulos de cámara y punch-ins.

**D · `DewSc9dgI9g` (103 s, collage)**
- Estética scrapbook: textura de papel, cinta adhesiva, polaroids, pegatinas, cabeza recortada, bocadillo de pensamiento.
- Subtítulo mínimo: una sola palabra, pequeña, en itálica manuscrita.
- Palabras clave enormes en serif amarilla ("CREATIVITY", "POSSIBILITIES").
- Intersticiales a pantalla completa en papel cuadriculado con texto de máquina de escribir.
- Los gráficos ocupan la mitad superior y nunca tapan la cara.

### Reglas comunes (el "estilo" a codificar)

1. **Dos niveles de texto.** Subtítulo pequeño y discreto (palabra a palabra) + palabras clave enormes, reservadas para 1 concepto cada pocos segundos. Nunca todo en grande.
2. **Profundidad.** Las palabras grandes van detrás de la persona (máscara) o detrás de objetos de la escena.
3. **Paleta derivada del metraje** (paredes, ropa) + un solo acento. La tipografía y las tarjetas usan esa paleta.
4. **Pareja tipográfica con contraste**: display (serif editorial o grotesca extendida) + itálica/script para la palabra que cambia el sentido.
5. **La cara nunca se tapa.** Los gráficos van en el tercio superior, a los lados o detrás.
6. **Cada concepto se ilustra** con un objeto diseñado dentro del mundo del vídeo (tarjeta, nota, interfaz, recorte), con sombra, inclinación y textura, no con iconos genéricos.
7. **Algo cambia cada 2–4 s**: punch-in, ángulo, insert, intersticial o color.
8. **Transiciones con motivo**: barrido de color, zoom con desenfoque, B/N → color.

### Diagnóstico del reel previo (`lesion-hombro`)

Está bien cortado y sincronizado, pero es estilo Hormozi: subtítulos pesados amarillo y blanco en cada frase, todo delante, sin etalonaje, gráficos genéricos (etiquetas rojas, medidor de dolor) y el mismo plano medio todo el rato. Lo que falta coincide con las reglas 1, 2, 3, 6 y 7.

## 4. Pipeline propuesto

Fusiona tu flujo (tomas + comentarios → storyboard → edición en Remotion) con lo mejor de las fuentes:

1. **Ingesta.** Contact sheet de cada toma, `ffprobe`, y transcripción con timestamps por palabra (Whisper local o ElevenLabs Scribe).
2. **Guion reconstruido.** La mejor toma de cada frase, sin pausas muertas. Se re-transcribe el corte para verificar que no se ha comido ninguna palabra (el bug más común según varias fuentes).
3. **Look.** Se extraen la paleta y el etalonaje del metraje y se propone una pareja tipográfica.
4. **Storyboard.** Una página con una viñeta por beat. Cada viñeta es un fotograma real de tu toma con la composición encima (texto detrás, tarjeta, subtítulo), más el texto, la transición y el SFX. **No se renderiza nada hasta que lo apruebes.**
5. **Máscara de persona** de los planos con texto detrás.
6. **Composición en Remotion**, por capas: metraje graduado → texto de fondo → persona (máscara) → tarjetas/gráficos → subtítulo → grano y viñeta.
7. **QA automático.** Contact sheet por beat + tira de fotogramas en cada corte + `ffprobe` (1080×1920, h264, yuv420p, audio). Checks: cara tapada, texto fuera de la zona segura, palabras cortadas, saltos de audio.
8. **Revisiones** por timestamp. Cada corrección de estilo se guarda como regla del skill.

Configuración de modelo: Opus 5.5 con esfuerzo **xhigh** para el storyboard y la primera versión, **medio** para retoques. Sesión nueva con resumen de traspaso pasados ~200K tokens. Un render a la vez.

## 5. Piezas técnicas y opciones

| Pieza | Opción local/gratis | Opción de pago/mejor | Nota |
|---|---|---|---|
| Transcripción | whisper.cpp (vía Remotion) o mlx-whisper en tu M3 Pro | ElevenLabs Scribe (lo usa video-use) | Español; el reel previo ya usó Whisper corregido. |
| Máscara de persona (texto detrás) | Apple Vision (segmentación de personas nativa de macOS), RVM, MatAnyone 2 | fal.ai BiRefNet video, BEN v2 | Hay que probarlo en un spike con tu metraje. El pelo y las manos rápidas son lo difícil. |
| Etalonaje | ffmpeg (`lut3d`, `eq`, curvas) con LUTs `.cube` | LUTs de pago | Las LUTs son lo más predecible para un agente. |
| Subtítulos | `@remotion/captions` (`createTikTokStyleCaptions`) | — | Ya instalado en el proyecto previo. |
| Tipografías | Google Fonts | Fuentes con licencia de la marca | |
| Música / SFX | Pixabay | Artlist / Epidemic | Regla tomada de las fuentes: cada sonido tiene que significar algo. |
| Imágenes para ilustrar conceptos | Recortes de tu propio B-roll, capturas reales | Generación de imagen (requiere API) | Las fuentes recomiendan assets reales. |

## 6. Skill propio a construir: `reel-editor`

No conviene instalar varios skills de terceros a la vez: se pisan entre sí. Propongo **un skill propio** en `Reels/.claude/skills/reel-editor/` que destile:

- `SKILL.md`: el pipeline de §4 y sus puertas (storyboard aprobado, QA superado).
- `STYLE.md`: las reglas de §3 + la marca EnsoMovers. Crece con cada corrección tuya.
- `MOTION.md`: reglas de movimiento (de claude-remotion-skill y aiidelist). Nunca interpolación lineal (springs/bezier), entradas que animan 2–3 propiedades a la vez, escalonado, salidas más rápidas que las entradas, micro-movimiento en reposo, todo el timing derivado de `fps`, un solo `theme.ts`, 300–600 ms de quietud antes de una revelación, titulares legibles al menos 1,2 s, sin aleatoriedad sin semilla.
- `scripts/`: contact sheets, `timeline_view`, verificación de render, máscara y LUT.
- Una plantilla de proyecto Remotion reutilizable (la del reel previo, limpiada).

Se instalan solo los skills oficiales de Remotion (ya está `remotion-best-practices`). video-use se toma como referencia de código, no como skill activo.
