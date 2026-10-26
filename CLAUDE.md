# Edición de reels EnsoMovers

Repositorio `edicion-enso`: el kit para editar los reels de Instagram de EnsoMovers con Claude Code. Se trabaja siempre desde esta carpeta, y cada reel vive en su propia subcarpeta (`Pancake/`, …), que no se sube a git.

- **Instalación:** si falta algo (`node_modules/`, el comando `mlx_whisper`, Satoshi en `.claude/skills/reel-editor/marca/fuentes/`), sigue [INSTALAR.md](INSTALAR.md).
- **Editar un reel:** usa el skill **reel-editor** (`.claude/skills/reel-editor/`). Ahí están el flujo, el estilo, la marca y los scripts. Las tomas nuevas llegan a la bandeja `tomas/`; las referencias visuales, a `referencias/`.
- **Idioma:** español, tanto con el usuario como en los textos del reel.
- **Las tomas son del usuario:** las de `<Reel>/tomas/` son de solo lectura. Las de la bandeja `tomas/` solo se mueven a su reel en el paso 0 del skill.
- **Presupuesto:** una sesión de Claude (5 h de uso) tiene que dar para un reel entero. Sigue las reglas de presupuesto del skill y prefiere herramientas locales a servicios de pago.
- **Remotion es compartido** (`package.json` en esta carpeta). Antes de actualizarlo, comprueba que los reels en curso siguen renderizando.
- **Lo aprendido se comparte:** al terminar un reel, si cambiaron el skill o `lib/` (correcciones en "Aprendido" de STYLE.md, componentes nuevos), propón al usuario hacer commit y push, para que todo el equipo edite con el mismo estándar.
