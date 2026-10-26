# edicion-enso

Kit de edición de vídeos cortos (reels de Instagram) de **EnsoMovers** con Claude Code.

Grabas y recortas tus tomas; Claude las transcribe, hace el corte, te propone un storyboard con fotogramas reales y, cuando lo apruebas, monta el reel con la identidad visual de EnsoMovers: títulos detrás de ti, tarjetas, trazos a mano, subtítulos, etalonaje, efectos de sonido. Te entrega un MP4 listo para subir.

Todo funciona en tu ordenador, sin servicios de pago aparte de tu suscripción a Claude.

---

## Qué necesitas

- Un **Mac con chip Apple** (M1, M2, M3 o posterior) con macOS 14 o superior.
- Una suscripción a **Claude Pro o Max** (la de claude.ai).
- Acceso a este repositorio en GitHub: pide al dueño que invite a tu cuenta.
- Unos 10 GB libres y conexión a internet durante la instalación.

---

## Instalación (una sola vez)

### 1. Abre la Terminal

Pulsa `⌘ Cmd` + `Espacio`, escribe **Terminal** y pulsa `Intro`. Se abre una ventana donde se escriben comandos.

### 2. Instala Claude Code

Copia esta línea, pégala en la Terminal y pulsa `Intro`:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Cuando termine, **cierra la Terminal y ábrela de nuevo**.

### 3. Ve a la carpeta donde quieras guardar el kit

Por ejemplo, Documentos:

```bash
cd ~/Documents
```

Si prefieres otra carpeta (por ejemplo, un disco externo con tus vídeos), escribe `cd ` (con un espacio al final), **arrastra la carpeta desde el Finder a la ventana de la Terminal** y pulsa `Intro`.

### 4. Abre Claude Code

```bash
claude
```

La primera vez te pedirá iniciar sesión: sigue los pasos en el navegador con tu cuenta de Claude.

### 5. Pásale a Claude esta instrucción

Copia este texto, pégalo en Claude y pulsa `Intro`:

```text
Clona el repositorio https://github.com/paubanon/edicion-enso en esta carpeta, entra en él y sigue su INSTALAR.md para instalar todas las dependencias y el material. Avísame cuando necesites que haga algo yo.
```

Claude instalará todo. Algunas veces te pedirá que hagas tú algo: pulsar **Instalar** en una ventana de Apple, escribir la contraseña de tu Mac (no se ve mientras escribes; es normal) o iniciar sesión en GitHub. Al acabar te dirá qué quedó instalado.

---

## Uso diario: editar un reel

1. **Recorta tus tomas** y déjalas en una carpeta con el nombre del reel dentro de `tomas/` (por ejemplo `edicion-enso/tomas/Hombro/`), con los nombres que explica [tomas/README.md](tomas/README.md) (`1.mp4`, `2.mp4`, `1_b_descripcion.mp4`…).
2. **Abre la Terminal en la carpeta del kit** (`cd` + arrastrar la carpeta `edicion-enso`, como en el paso 3) y escribe `claude`.
3. **Escribe** `/reel-editor`, seguido de tus comentarios. Por ejemplo:

   ```text
   /reel-editor Hombro. Va sobre la movilidad de hombro. La toma 4 tiene que ir con humor, y en la 7 me gustaría un gráfico del rango de movimiento.
   ```

4. Claude transcribirá y cortará las tomas y **abrirá un storyboard en el navegador**: una imagen por momento del reel, con el diseño encima. Coméntalo por número de escena hasta que te guste y dile **"aprobado"**.
5. Claude monta el reel y lo deja en `finales/<NombreDelReel>.mp4`. Pídele cambios por tiempo ("en 0:12 el título sale tarde") hasta que esté listo.
6. Sube el vídeo a Instagram y añade ahí la música en tendencia: el reel sale sin música a propósito.

### Consejos

- **Referencias:** si ves un reel cuyo estilo te encanta, descárgalo y déjalo en `referencias/`. Claude lo analizará en la siguiente edición.
- **Sesiones largas:** si Claude te dice que la conversación es muy larga, escribe `/clear` y vuelve a invocar `/reel-editor <NombreDelReel>`. Retoma donde lo dejó gracias al archivo `handoff.md` del reel.
- **Lo que aprende se comparte:** cada corrección de estilo que le hagas queda guardada en el kit. Cuando Claude te proponga "subir los cambios", di que sí, para que el resto del equipo edite con el mismo estándar.
- **Actualizar el kit:** pídele a Claude "actualiza el repositorio" para traer las mejoras de los demás.

---

## Qué hay dentro

| Carpeta o archivo | Qué es |
|---|---|
| `tomas/` | Tus tomas recortadas, una carpeta por reel (`tomas/Pancake/`, `tomas/Hombro/`…) |
| `ediciones/` | Lo que genera Claude para cada reel: corte, storyboard, código y borradores |
| `finales/` | Los reels terminados, listos para subir |
| `referencias/` | Reels de referencia visual (no se suben a GitHub) |
| `.claude/skills/reel-editor/` | El skill de edición: flujo (`SKILL.md`), estilo (`STYLE.md`), movimiento (`MOTION.md`), storyboard (`STORYBOARD.md`) y scripts |
| `.claude/skills/reel-editor/marca/` | Identidad de EnsoMovers para vídeo: reglas (`MARCA.md`), fuentes, logos del ensō y efectos de sonido |
| `lib/` | Componentes de Remotion reutilizables (títulos, tarjetas, subtítulos, trazos, recortes…) |
| `docs/` | Investigación de partida sobre edición con Claude |
| `INSTALAR.md` | Instrucciones de instalación para Claude |
| `CLAUDE.md` | Reglas generales que Claude lee siempre en esta carpeta |

Por cada reel hay tres sitios: `tomas/<Reel>/` (lo que grabas tú y nadie toca), `ediciones/<Reel>/` (el trabajo de Claude; se puede borrar sin perder tus tomas) y `finales/<Reel>.mp4` (el resultado). Todo eso se queda en tu ordenador: a GitHub solo sube el kit.

---

## Para el agente

Si eres Claude Code y acabas de llegar a este repositorio: la instalación está en [INSTALAR.md](INSTALAR.md) y las reglas generales en [CLAUDE.md](CLAUDE.md). Para editar un reel, usa el skill `reel-editor`.
