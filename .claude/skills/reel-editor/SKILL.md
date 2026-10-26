---
name: reel-editor
description: Edita reels verticales de EnsoMovers (talking head + B-roll) con Remotion y acabado de editor profesional - ingesta y transcripción de tomas, corte, storyboard con fotogramas reales para aprobar, títulos detrás de la persona, etalonaje, gráficos que ilustran conceptos, QA y render. Úsalo cuando el usuario pase tomas de un reel, pida un storyboard, una edición, una revisión o un render de un reel.
---

# Editor de reels EnsoMovers

El usuario graba; tú cortas, diseñas y compones encima en Remotion. Nunca alteras su voz ni su imagen más allá del corte, el encuadre y el etalonaje.

Lee también, cuando toque: [marca/MARCA.md](marca/MARCA.md) y [STYLE.md](STYLE.md) (antes del storyboard), [STORYBOARD.md](STORYBOARD.md) (formato del storyboard), [MOTION.md](MOTION.md) (antes de escribir animación). Para la API de Remotion, el skill `remotion-best-practices`.

## Espacio de trabajo

```
<raíz del repo>/             ← directorio de trabajo (repo edicion-enso); aquí se ejecuta todo
  package.json, node_modules Remotion 4 compartido por todos los reels
  lib/                       componentes compartidos: Footage (metraje + capas detrás + reencuadres), BigTitle, Captions, Card + Marker (tarjeta estándar, marcador sage), BrushStroke (trazo a mano), BRoll, Sticker (objeto recortado como pegatina), Sfx (catálogo de efectos), Finish, theme
  tomas/                     bandeja de entrada: el usuario deja aquí las tomas recortadas del próximo reel
  referencias/               reels de referencia visual que añade el usuario (análisis en STYLE.md)
  <Reel>/
    tomas/                   tomas del usuario. Solo lectura: nunca mover, renombrar ni borrar
    edit/                    notas.md, transcripción, cut.json, storyboard.json/.html, handoff.md
    public/                  main_cut.mp4, cutout.webm, B-roll, sfx, música, marca → skill/marca (fuentes, logos)
    src/                     index.ts, Root.tsx, Reel.tsx, edit.ts, edit.json, components/
    out/                     stills, renders y QA
```

`S=.claude/skills/reel-editor/scripts`. `cut.py` se lanza con `uv run` (declara numpy); el resto, con `python3`. La transcripción usa el `mlx_whisper` instalado en el sistema (`uv tool`).

### Nombres de las tomas (convención del usuario)

- `1.mp4`, `2.mp4`… → frase del guion, en orden. `6.1`, `6.2`, `6.3` → partes (o tomas alternativas) de la frase 6.
- `1_b_espalda_curvada.mp4` → B-roll de la frase 1; la letra (`b`, `c`…) distingue varios B-roll de una misma frase y el resto describe el contenido.
- `11_pendiente_ilustrar.MP4` → toma de voz con una nota para ti: aquí, que esa frase hay que ilustrarla con gráficos.
- `ingest.py` interpreta esto y lo vuelca en `edit/clips.md` (papel y nota por toma). Si un nombre no encaja, pregunta.

## Presupuesto: la sesión de 5 h tiene que dar para un reel entero

- Lee `edit/transcript.md` y `edit/cut_transcript.md`, nunca `edit/words/*.json`.
- Mira solo las imágenes pequeñas que generan los scripts. Una hoja de contacto en vez de diez fotogramas.
- Comprueba con `remotion still` (`--scale=0.3`) solo uno o dos fotogramas sueltos: cada still vuelve a empaquetar el proyecto (~25 s). Para revisar todo el reel, un borrador `--scale=0.5` (~5 min para 90 s) y extrae los fotogramas clave con ffmpeg (`-ss <t> -frames:v 1`, uno por archivo, y luego `tile`). Render completo a resolución final: solo para entregar.
- No releas archivos que ya tienes en contexto; cambia con Edit, no reescribas.
- No abras Studio salvo que te lo pida; el usuario puede abrirlo con el comando de abajo.
- Un render a la vez.
- Si la conversación supera ~200K tokens, escribe `edit/handoff.md` (estado, decisiones, siguiente paso, rutas) y pide al usuario que haga `/clear` y vuelva a invocarte.

## Flujo, con dos puertas que requieren aprobación

**0. Preparar el reel** (si `<Reel>/src` no existe). Si las tomas están en la bandeja `tomas/` de la raíz, pregunta el nombre del reel (una palabra, p. ej. `Pancake`) y muévelas a `<Reel>/tomas/`, dejando el `README.md` de la bandeja en su sitio:
```bash
mkdir -p <Reel>/{tomas,edit,public,src,out} && ln -sfn ../../.claude/skills/reel-editor/marca <Reel>/public/marca
find tomas -maxdepth 1 -type f ! -name README.md ! -name '.*' -exec mv {} <Reel>/tomas/ \;
cp .claude/skills/reel-editor/template/* <Reel>/src/
```
Si hay referencias nuevas en `referencias/` que no estén analizadas en STYLE.md, analízalas primero (hoja de contacto de cada una) y propón qué tomar de ellas.

**1. Ingesta.** `python3 $S/ingest.py <Reel> --vocab "EnsoMovers, …"` (añade términos del tema; ~1/4 de la duración, lánzalo en segundo plano). Lee `edit/clips.md`, `edit/transcript.md`, `edit/overview.jpg` y los comentarios del usuario (`edit/notas.md` o el chat).

**2. Corte.** Escribe `edit/cut.json` (formato en el docstring de `cut.py`): las tomas y rangos en orden, la mejor toma de cada frase, sin repeticiones. `uv run $S/cut.py <Reel>`. Si avisa de palabras cortadas, ajusta los rangos y repite. Una palabra de Whisper de más de ~0,7 s suele esconder una repetición o un ruido (respiración, roce al moverse): compruébalo con la energía de la toma y sácalo partiendo el rango. Lee `edit/cut_transcript.md`: es tu mapa de fotogramas para todo lo demás.

**3. Storyboard → PUERTA 1.** Lee STYLE.md y STORYBOARD.md. Escribe `edit/storyboard.json` y `python3 $S/storyboard.py <Reel> --open`. Resume al usuario en pocas líneas la idea, el look y los momentos clave. No construyas nada hasta que lo apruebe. En las iteraciones cambia solo los beats que comente.

**4. Recorte de persona.** Si algún beat tiene título detrás: `python3 $S/cutout.py <Reel>` (unos 2–3 min por minuto de vídeo; lánzalo en segundo plano y sigue construyendo).

**5. Construcción.** `src/Reel.tsx` con la pila de capas de STYLE.md y los componentes de `lib/`. Lo que sea propio del reel va en `src/components/`. Para traer un objeto del B-roll al plano del que habla: `scripts/object_cutout.swift` (uso en su cabecera; compílalo con `swiftc -O` en `scripts/.build/`) → PNG en `public/objetos/` → `lib/Sticker`. Si algo es claramente reutilizable, llévalo a `lib/`. Fotogramas desde `cut_transcript.md`. `npm run typecheck`.

**6. Verificación.** Borrador a media escala y hoja de fotogramas clave; arregla. Después render completo (~9 min para 90 s), `python3 $S/qa.py <Reel>/out/<reel>.mp4 --at <t1>,<t2>,…` y mira la hoja de contacto. Comprueba: cara nunca tapada, texto dentro de la zona segura, nada cortado, títulos legibles al menos 1,2 s, el gancho se entiende en silencio. Arregla antes de enseñar.

**7. Revisión → PUERTA 2.** Entrega la ruta del MP4. El usuario comenta por tiempo ("en 0:12…"). Retoca y re-renderiza. **Cada corrección de estilo que valga para futuros reels se añade a la sección "Aprendido" de STYLE.md, con el porqué.**

## Comandos de Remotion (desde la raíz del repo)

```bash
npx remotion studio <Reel>/src/index.ts --public-dir=<Reel>/public
npx remotion still <Reel>/src/index.ts Reel <Reel>/out/f<N>.jpg --frame=<N> --scale=0.5 --public-dir=<Reel>/public
npx remotion render <Reel>/src/index.ts Reel <Reel>/out/<reel>.mp4 --public-dir=<Reel>/public
```

## Audio

- La voz sale de `cut.py` ya procesada y normalizada a −14 LUFS. Música y efectos van con `<Audio>` de `@remotion/media`, desde `public/`.
- Música bajo la voz: unos 18–20 dB por debajo. Ducking solo si se nota.
- Cada efecto de sonido tiene un motivo visible (entra un título, una tarjeta, un corte). Nada de whooshes por defecto.
- Por defecto **no hay música**: el usuario añade una canción en tendencia desde Instagram al publicar. Deja la voz limpia y sin cama musical salvo que te pase un archivo.
- Efectos de sonido: biblioteca compartida en `marca/sfx/` (`staticFile("marca/sfx/…")`; lista en `marca/sfx/LEEME.md`). Pocos y discretos, como pide la marca. No los sintetices ni uses otros.
