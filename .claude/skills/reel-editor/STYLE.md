# Estilo EnsoMovers

Objetivo: edición de editor profesional con toques cinematográficos, en la que **cada fotograma funcione como imagen por sí mismo**. Las referencias están en `referencias/` (análisis abajo).

**La síntesis:** la energía y la profundidad de las referencias, con la contención de la marca. Editorial científica con calma: pocos elementos, perfectamente puestos, cada uno con un propósito ("si un elemento visual no comunica nada, se elimina"). Dinámico por el ritmo del corte y la tipografía, no por efectos.

## Marca

Todo en [marca/MARCA.md](marca/MARCA.md): paleta Luminous Enso Pure, Satoshi + Fira Sans + JetBrains Mono, logo ensō. Lo esencial para reels:
- Texto sobre el vídeo: **blanco con sombra amplia** y la palabra clave en **sage**, también sobre paredes claras (ver Aprendido). Texto en tarjetas: negro, con la palabra clave sobre un **marcador sage**.
- Datos medibles (grados, repeticiones, semanas) en JetBrains Mono: es el sello de "editorial científica".
- Nada de filtros agresivos, neón ni texto sobrecargado. Transiciones contenidas.
- El logo aparece una sola vez como mucho, normalmente al cierre, y nunca tapa el gancho.

## Las reglas

1. **Dos niveles de texto.**
   - Subtítulo discreto (`lib/Captions`): pequeño, palabra activa en acento, a la altura del pecho.
   - Título enorme (`lib/BigTitle`): reservado para un concepto cada pocos segundos.
   - El subtítulo se oculta mientras hay un título o tarjeta protagonista. Nunca todo en grande.
   - El subtítulo va en Fira Sans Bold blanco con sombra amplia, palabra activa en sage, sin píldora.
2. **Profundidad.** Los títulos grandes van **detrás de la persona** (capa `behind` de `Footage`) o detrás de objetos de la escena. Se colocan donde hay fondo libre: pared sobre la cabeza, lados. Si en el plano la cabeza llega a menos de ~300 px del borde superior, no hay sitio para un título detrás (la cabeza taparía la palabra): usa subtítulo, una tarjeta delante sobre el torso o un intertítulo.
   **Legibilidad sobre pared clara:** la sombra amplia (`textShadow` en theme) es la que separa el blanco de la pared; si aun así no se lee, sube el tamaño, coloca el título sobre una zona más oscura o baja las altas luces del etalonaje. Compruébalo en el storyboard, no en el render.
3. **La cara nunca se tapa.** Los gráficos van en el tercio superior, a los lados o detrás. Todo dentro de la zona segura (`safeZone` en theme).
4. **Pareja tipográfica con contraste.** Satoshi Bold en mayúsculas para el título + Fira Sans Light Italic en sage para la palabra que cambia el sentido (estilos `display` / `contrast` / `data` de `BigTitle`). Mezclarlas dentro de una misma frase es el recurso estrella.
5. **Cada concepto se ilustra.** Un objeto diseñado dentro del mundo del vídeo, animado en Remotion: tarjeta, nota, checklist, contador, cronómetro, diagrama de cuerpo, interfaz, recorte del B-roll. Con sombra, inclinación y textura, no iconos genéricos. Va ligado a la palabra exacta en que se dice.
   - **Etiqueta estándar = tarjeta:** fondo blanco roto (`colors.card`), sombra, giro leve, línea mono pequeña en earth (meta) + título Satoshi en mayúsculas, con insignia ✓ sage / ✕ earth si es un juicio. Nunca una etiqueta mínima de una línea.
   - **Dibujos sobre el plano** (flechas, círculos, trayectorias): trazo de pincel a mano, como dibujado en un iPad encima del frame, blanco con sombra, que se dibuja con el sonido de escritura.
6. **Algo cambia cada 2–4 s.** Punch-in, cambio de plano, insert, intersticial, cambio de color. El primer 1,5 s nunca es un talking head estático: el gancho es visual y se entiende sin sonido.
7. **Transiciones con motivo y pocas** (la marca pide reels minimalistas, "sin transiciones excesivas"): corte seco por defecto. Solo en cambios de idea, una de estas: zoom con desenfoque suave, blanco y negro → color, un objeto que conecta dos escenas, barrido en negro o mist.
8. **Etalonaje con intención.** Luz natural, cálida y suave (manual de marca). Contraste ligeramente subido, piel natural y negros con cuerpo. Nunca un look "mood" agresivo. Grano y viñeta sutiles (`lib/Finish`) para unir metraje y gráficos. Si el metraje está frío o plano, se corrige con `colorCorrection` en `Footage`.
9. **Intersticiales a pantalla completa** (negro o mist, nunca sage de fondo) solo para cambios de capítulo o el remate. Máximo 1–2 por reel.
10. **Cierre.** Una CTA clara (comentar, guardar, seguir) en el diseño del reel, no una pantalla genérica.

## Pila de capas (de abajo arriba)

metraje etalonado → títulos detrás → persona recortada → tarjetas y gráficos → subtítulo → grano y viñeta

## Referencias analizadas

- **A `DcbgKLeMcXK`** – Título fijo "hook" en sans blanca pesada con número en script itálica amarilla. El título queda detrás de lo que hay en escena (el poste tapa la "o"). Clones con estela de movimiento. Listas de interfaz flotando en 3D alrededor de él.
- **B `DdhoUcHuHCH`** – Tipografía cinética con una combinación distinta por frase. Barrido circular de color. Blanco y negro → color. El texto siempre por encima de la cabeza.
- **C `DehbdDYssBE`** – Paleta sacada de la habitación (verde + crema + magenta del jersey). Números serif enormes detrás de la cabeza. Subtítulo en píldora pequeña. Tarjetas editoriales (calendario, checklist tachada, waitlist). Tarjeta de título a pantalla completa. Zoom con desenfoque.
- **D `DewSc9dgI9g`** – Collage de papel: cinta, polaroids, pegatinas, cabeza recortada. Subtítulo de una palabra manuscrita. Palabras clave enormes en serif amarilla. Intersticiales de papel cuadriculado.

La C es la más cercana a la marca: cambia su verde y crema por negro, mist y sage, y su serif por Satoshi. De la A se toma el título integrado en la escena. De la B, la tipografía cinética, pero con una sola familia de estilos. De la D, solo la idea de ilustrar con objetos; su estética de collage choca con la marca ("informalidad descuidada").

## Lo que no queremos (reel `lesion-hombro`)

Subtítulos pesados amarillos y blancos con contorno en cada frase, todo delante de la persona, sin etalonaje, etiquetas rojas genéricas y el mismo plano medio todo el rato.

## Aprendido

Correcciones del usuario que aplican a todos los reels, con su porqué. Añadir al final, sin borrar.

- **2026-10-25 · Pancake.** Títulos y subtítulos en **blanco con sombra amplia**, nunca en negro, aunque la pared sea blanca. **Por qué:** el texto negro sobre fondo claro le resulta poco atractivo y poco profesional, aunque tenga más contraste; prima la estética sobre el contraste estricto del manual.
- **2026-10-25 · Pancake.** Subtítulo en **otra fuente que los títulos** (Fira Sans Bold), sin píldora. **Por qué:** la píldora clara con texto negro no le resultaba atractiva.
- **2026-10-25 · Pancake.** Las etiquetas tipo «✓ esto» de una línea son **demasiado básicas**: siempre tarjeta completa (meta mono + título + sombra), como las tarjetas de «vídeos de internet». **Por qué:** es el diseño que le gustó.
- **2026-10-25 · Pancake.** Tarjetas y recuadros **más blancos que mist** (`#F8F9F7`). **Por qué:** con una imagen muy luminosa, el mist parece gris y apagado.
- **2026-10-25 · Pancake.** Flechas y dibujos **a mano, como pincel en iPad**, en blanco con sombra. **Por qué:** las flechas negras de línea se perdían contra su pelo y parecían frías.
- **2026-10-25 · Pancake.** Citas y textos que acompañan a la voz **aparecen a la vez que lo dice**, palabra a palabra. El marcador de una palabra clave se pinta **con el sonido de subrayado**.
- **2026-10-25 · Pancake.** Un montaje rápido de B-roll va **sobre la voz continua**: cambia la imagen, el audio no se corta.
- **2026-10-25 · Pancake.** **Diálogo continuo**: ningún silencio entre frases ni dentro de ellas, tampoco para "demostraciones"; él demuestra mientras habla. `tighten: false` solo si el usuario pide un silencio. **Por qué:** los huecos rompen el ritmo del reel.
- **2026-10-25 · Pancake.** **No oscurecer el metraje.** Como mucho, `highlights` −0,1 y viñeta muy suave; la imagen luminosa es parte del look. **Por qué:** con −0,3 en altas luces y viñeta 0,25, algunas tomas quedaban oscuras.
- **2026-10-25 · Pancake.** Un gráfico entra **cuando se dice su idea, nunca antes** (la flecha del error, en «hacia el suelo», no en «intentar»). Lo que se mueve con la frase (deslizadores, etiquetas) arranca en la **primera palabra** de lo que nombra («bicho palo», «Circo del Sol»), no en la última.
- **2026-10-25 · Pancake.** Mientras él habla a cámara, **no tapar su plano con B-roll** para ilustrar objetos: recortar los objetos y traerlos a su plano (aparecen junto a él). **Por qué:** con el B-roll encima él queda estático y se pierde su presencia.
- **2026-10-25 · Pancake.** **Recortar el material de rodaje** que se vea (trípodes, focos) con un reencuadre del plano.
- **2026-10-25 · Pancake.** Pantallas partidas y cutaways se mantienen **al menos ~1 s después de su último elemento**; si la frase se acaba, se alargan sobre el principio de la siguiente.
- **2026-10-25 · Pancake.** Las bromas se ilustran con la **idea**, no con el literal: «te voy a dar un ejercicio. No. Uno» → tarjetas flotantes con muchos ejercicios que se tachan y queda uno, no un «1» que tiembla.
- **2026-10-25 · Pancake.** Flechas: el gesto erróneo, recto hacia abajo; el correcto, **hacia delante y suave**, casi horizontal, que cae poco a poco (como una exponencial decreciente), no un arco.
