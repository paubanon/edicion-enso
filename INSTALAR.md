# Instalación (instrucciones para el agente)

Estas instrucciones son para Claude Code. Quien te las pasa no es técnico: haz tú todo lo que se pueda hacer desde la terminal, explícale en una frase llana cada vez que necesites que haga algo (pulsar un botón, escribir su contraseña) y, al terminar, dale el resumen del último paso.

Ejecuta los pasos en orden. Antes de instalar cada cosa, comprueba si ya está; no reinstales lo que funciona.

## 0. Requisitos

- **Mac con Apple Silicon** (M1 o posterior) y macOS 14 o superior: `uname -m` debe decir `arm64`; `sw_vers -productVersion`, ≥ 14. La transcripción (MLX) y el recorte de personas y objetos (Apple Vision) solo funcionan ahí. Si no se cumple, para y explícaselo.
- Unos 10 GB libres (modelo de transcripción, Remotion y navegador de render).

## 1. Repositorio

Si aún no estás dentro del repositorio, clónalo en la carpeta actual y entra:

```bash
gh repo clone paubanon/edicion-enso || git clone https://github.com/paubanon/edicion-enso.git
cd edicion-enso
```

El repositorio es privado. Si falla por permisos:
- Si no hay `gh`, instálalo con Homebrew (paso 3) y vuelve aquí.
- Pide a la persona que ejecute `! gh auth login` en esta misma sesión (el `!` lo lanza en su terminal) y siga los pasos del navegador. Su cuenta de GitHub tiene que estar invitada al repositorio por su dueño.

## 2. Herramientas de desarrollador de Apple

```bash
xcode-select -p
```

Si falla, ejecuta `xcode-select --install`, pide a la persona que pulse **Instalar** en la ventana que aparece y espera a que termine (varios minutos). Aportan `git`, `swiftc` y Python.

## 3. Homebrew y paquetes del sistema

Si `brew` no existe, Homebrew pide la contraseña del Mac de forma interactiva, así que no puedes lanzarlo tú. Pide a la persona que ejecute en esta sesión:

```
! /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

y después añade Homebrew al PATH de su shell (`eval "$(/opt/homebrew/bin/brew shellenv)"` en `~/.zprofile`, si el instalador no lo hizo).

Después instala lo que falte:

```bash
brew install ffmpeg node@22 python uv gh
brew link --overwrite node@22   # solo si `node -v` no da ≥ 20.19
```

Comprueba que `ffmpeg -version`, `node -v` (≥ 20.19 o ≥ 22.13), `python3 --version` (≥ 3.10) y `uv --version` responden.

## 4. Transcripción local (Whisper en MLX)

```bash
uv tool install mlx-whisper
uv tool update-shell   # añade ~/.local/bin al PATH si hace falta
```

Descarga el modelo ahora (~1,6 GB) para que la primera edición no espere:

```bash
ffmpeg -v error -f lavfi -i "sine=frequency=440:duration=2" /tmp/enso-prueba.wav
mlx_whisper /tmp/enso-prueba.wav --model mlx-community/whisper-large-v3-turbo --language es --output-dir /tmp --verbose False
```

## 5. Fuente Satoshi (no viene en el repositorio)

Su licencia prohíbe redistribuirla, así que se descarga gratis de Fontshare en cada equipo:

```bash
mkdir -p /tmp/satoshi && curl -sSL -o /tmp/satoshi/satoshi.zip https://api.fontshare.com/v2/fonts/download/satoshi
unzip -o -q /tmp/satoshi/satoshi.zip -d /tmp/satoshi
cp /tmp/satoshi/*/Fonts/TTF/Satoshi-Variable.ttf /tmp/satoshi/*/Fonts/TTF/Satoshi-VariableItalic.ttf .claude/skills/reel-editor/marca/fuentes/
```

## 6. Remotion

```bash
npm ci
npx remotion browser ensure   # navegador con el que Remotion renderiza
npm run typecheck
```

## 7. Herramientas de recorte (Apple Vision)

Compílalas una vez para comprobar que Swift funciona (`cutout.py` también las compila sola si faltan):

```bash
mkdir -p .claude/skills/reel-editor/scripts/.build
swiftc -O .claude/skills/reel-editor/scripts/person_mask.swift -o .claude/skills/reel-editor/scripts/.build/person_mask
swiftc -O .claude/skills/reel-editor/scripts/object_cutout.swift -o .claude/skills/reel-editor/scripts/.build/object_cutout
```

## 8. Comprobación final y resumen

Repasa que todo responde: `ffmpeg`, `node`, `uv`, `mlx_whisper --help`, Satoshi en `marca/fuentes/`, `npm run typecheck` sin errores y los dos binarios en `scripts/.build/`.

Después dile a la persona, en pocas líneas:
- qué quedó instalado y si algo falló (con la causa en lenguaje llano);
- cómo empezar: dejar las tomas recortadas en `tomas/` (con los nombres de `tomas/README.md`) y escribir `/reel-editor` seguido de sus comentarios sobre el reel;
- que cada vez que quiera editar, abra la terminal en esta carpeta y escriba `claude`.
