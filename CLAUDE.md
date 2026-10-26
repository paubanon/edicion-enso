# Edición de reels EnsoMovers

Repositorio `edicion-enso`: el kit para editar los reels de Instagram de EnsoMovers con Claude Code. Se trabaja siempre desde esta carpeta. Cada reel tiene sus tomas en `tomas/<Reel>/`, su edición en `ediciones/<Reel>/` y su versión entregada en `finales/<Reel>.mp4`. Nada de eso se sube a git.

- **Instalación:** si falta algo (`node_modules/`, el comando `mlx_whisper`, Satoshi en `.claude/skills/reel-editor/marca/fuentes/`), sigue [INSTALAR.md](INSTALAR.md).
- **Editar un reel:** usa el skill **reel-editor** (`.claude/skills/reel-editor/`). Ahí están el flujo, el estilo, la marca y los scripts. Las referencias visuales llegan a `referencias/`.
- **Idioma:** español, tanto con el usuario como en los textos del reel.
- **Las tomas son del usuario:** `tomas/` es de solo lectura; nunca muevas, renombres ni borres sus archivos.
- `ediciones/lesion-hombro/` es un reel antiguo con su propio proyecto de Remotion (su `package.json`, `node_modules` y scripts; las tomas originales están en `tomas/lesion-hombro/`). Se conserva como ejemplo de lo que no queremos (ver STYLE.md); no lo uses como base.
- **Presupuesto:** una sesión de Claude (5 h de uso) tiene que dar para un reel entero. Sigue las reglas de presupuesto del skill y prefiere herramientas locales a servicios de pago.
- **Remotion es compartido** (`package.json` en esta carpeta). Antes de actualizarlo, comprueba que los reels en curso siguen renderizando.
- **Lo aprendido se comparte:** al terminar un reel, si cambiaron el skill o `lib/` (correcciones en "Aprendido" de STYLE.md, componentes nuevos), propón al usuario hacer commit y push, para que todo el equipo edite con el mismo estándar.
