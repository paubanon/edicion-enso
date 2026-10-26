# Storyboard

Página HTML con un fotograma real del corte por beat y el diseño encima, para que el usuario apruebe la idea **antes** de construir nada. La genera `scripts/storyboard.py` a partir de `ediciones/<Reel>/edit/storyboard.json`.

## Qué es un beat

Un tramo de 2–5 s con **una sola función**: gancho, problema, ejemplo, giro, remate o CTA. Un reel de 60 s tiene unos 12–20 beats. Los tiempos son segundos de salida (de `cut_transcript.md`).

## storyboard.json

```json
{
  "title": "Pancake · 52 s",
  "summary": "Idea en una frase. Look: negro + sage sobre pared clara, cálido, grano suave. Tono: …",
  "look": { "grade": "contrast(1.08) saturate(1.05)" },
  "beats": [
    {
      "id": 1, "from": 0.0, "to": 2.4, "at": 1.1,
      "said": "¿Por qué no llegas al suelo en pancake?",
      "behind": "<div style='position:absolute;top:240px;width:100%;text-align:center'><div class='display' style='font-size:210px'>Pancake</div><div class='contrast' style='font-size:130px'>no es flexibilidad</div></div>",
      "front": "",
      "caption": false,
      "notes": "Gancho: título entra palabra a palabra detrás de la cabeza. Punch-in 1.15. SFX: golpe grave al entrar."
    },
    {
      "id": 2, "from": 2.4, "to": 5.0, "at": 3.6,
      "said": "El problema no son tus isquios",
      "behind": "",
      "front": "<div class='card' style='top:300px;left:60px;rotate:-2deg'><div class='row'><div class='badge no'>✕</div><div><div class='meta'>el problema no son</div><div class='title'>Tus isquios</div></div></div></div>",
      "caption": "el problema no son tus <b>isquios</b>",
      "notes": "Tarjeta de papel que entra desde la izquierda con giro; la palabra se tacha al decir «no son»."
    }
  ]
}
```

- `at`: segundo del fotograma que se muestra (por defecto, el centro del beat). Elige uno con buena expresión.
- `behind`: HTML que queda **detrás** de la persona; el script recorta la persona de ese fotograma y la pone encima.
- `front`: HTML por encima de todo (tarjetas, flechas, gráficos).
- `caption`: el subtítulo discreto (HTML, la palabra activa en `<b>`), o `false` si el beat lo oculta.
- `notes`: animación, transición de entrada, SFX y lo que no se ve en un fotograma fijo.

## Reglas del HTML

- Coordenadas en píxeles de composición (1080×1920) con `position:absolute`, igual que en Remotion.
- Clases disponibles, idénticas a los componentes y con las fuentes de la marca. Sobre el vídeo el texto sale blanco con sombra; dentro de `card` o `paper`, negro.
  - Texto: `display` (Satoshi Bold en mayúsculas), `contrast` (Fira Sans Light Italic), `data` (JetBrains Mono), `mark` (palabra clave: sage sobre vídeo, marcador sage en tarjeta), `caption` (la palabra activa en `<b>`).
  - Tarjeta estándar: `<div class='card' style='top;left;rotate'><div class='row'><div class='badge yes'>✓</div><div><div class='meta'>meta mono</div><div class='title'>Título</div></div></div></div>` (`badge no` para ✕; sin badge si no es un juicio).
  - Superficie clara a pantalla completa: `paper`. Trazo a mano: `<svg …><path class='stroke' d='…'/></svg>`.
  - Colores: `var(--black)`, `var(--white)`, `var(--card)`, `var(--mist)`, `var(--sage)`, `var(--earth)`.
- Una ilustración compleja (diagrama, interfaz) se maqueta de forma simple pero reconocible: formas y texto, no una caja con "aquí va X".
- Respeta la zona segura (la página tiene un interruptor para verla).

## Proceso

1. Escribe `storyboard.json` completo de una vez.
2. `python3 scripts/storyboard.py ediciones/<Reel> --open`. Fotogramas y recortes se cachean en `edit/storyboard/`.
3. Al usuario: 3–5 líneas con la idea, el look y los beats en los que más se juega. Espera su aprobación.
4. En los cambios, edita solo los beats comentados y regenera.
5. El storyboard aprobado es el contrato de la construcción: si algo cambia al construir, avisa.
