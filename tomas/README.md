# Tomas

Aquí van tus **tomas ya recortadas**, en **una carpeta por reel** con el nombre del reel:

```
tomas/
├── Pancake/
│   ├── 1.mp4
│   ├── 1_b_espalda_curvada.mp4
│   └── 2.mp4 …
└── Hombro/
    └── …
```

Claude nunca mueve, renombra ni borra lo que hay aquí: todo lo que genera va a `ediciones/<Reel>/`, y el vídeo terminado a `finales/<Reel>.mp4`. Para editar, abre Claude en la carpeta del kit y escribe `/reel-editor` seguido del nombre del reel (el de su carpeta) y tus comentarios.

## Cómo nombrar las tomas

El número es el orden del guion. Así Claude sabe qué va con qué sin que se lo expliques:

| Nombre | Qué significa |
|---|---|
| `1.mp4`, `2.mp4`, `3.mp4`… | Cada frase del guion, en orden |
| `6.1.mp4`, `6.2.mp4` | Partes (o tomas alternativas) de la frase 6 |
| `1_b_espalda_curvada.mp4` | B-roll (plano de recurso) de la frase 1, con una descripción corta |
| `1_c_otro_plano.mp4` | Otro B-roll de la misma frase (letra distinta) |
| `11_pendiente_ilustrar.mp4` | Toma con una nota para Claude: aquí, que esa frase hay que ilustrarla |

## Consejos de grabación

- Cámara quieta en cada plano y en vertical.
- Recorta el principio y el final de cada toma, pero deja medio segundo antes y después de hablar: el corte fino lo hace Claude.
- Si una frase tiene varias tomas, deja solo la buena o numéralas (`4.1`, `4.2`) y dile cuál prefieres.
- Evita que se vean focos, trípodes o cables; si se cuelan, Claude puede reencuadrar.

Los vídeos de esta carpeta no se suben a GitHub.
