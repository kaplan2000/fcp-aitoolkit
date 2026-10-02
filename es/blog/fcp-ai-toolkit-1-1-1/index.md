# FCP AI-Toolkit 1.1.1 ya está aquí: 1.1, más dos correcciones

Date: 2026-10-02
Status: Lanzamiento
Language: es
Canonical: https://www.fcp-aitoolkit.com/es/blog/fcp-ai-toolkit-1-1-1/

1.1.1 ya está en el Mac App Store con Smart Cache, edición de subtítulos, Smart Search y unos 100 idiomas. El “.1” extra es por dos errores que corregimos justo a tiempo.

FCP AI-Toolkit 1.1.1 está en el Mac App Store desde el 30 de septiembre. Si tienes la versión 1.0, esta es tu actualización. Abre el Mac App Store y actualiza como siempre.


Esta versión trata de una sola cosa: volver a un montaje sin empezar de cero. Pruebas otro estilo, recortas la intro, corriges un nombre, alargas un clip. Los subtítulos te siguen el ritmo, en lugar de empezar desde cero cada vez.



## Espera, ¿qué pasó con la 1.1?

Buena pregunta. El 22 de septiembre publicamos un avance titulado [Próximamente en 1.1](/es/blog/fcp-ai-toolkit-1-1-preview/). La versión 1.1 estaba terminada y revisada. Solo esperaba su vídeo de lanzamiento.


Entonces, el 25 de septiembre, hicimos una última ronda de pruebas con proyectos reales de Final Cut Pro. Varios clips, audio separado, el tipo de desorden que tiene un montaje de verdad. Aparecieron dos errores. Corregimos ambos el mismo día.


Podríamos haber publicado la 1.1 y parcheado después. Preferimos arreglar primero la compilación y darle un número nuevo. Así que 1.1.1 es simplemente la 1.1 más dos correcciones. Las funciones son exactamente las que describía el avance, y el “.1” extra representa los dos errores que detectamos antes de que pudieras encontrártelos.


Enviamos la 1.1.1 a Apple el 27 de septiembre y salió el 30. Nadie se perdió ninguna versión: nunca hubo una 1.1 pública. Si tienes la 1.0, pasas directamente a la 1.1.1.


- 21 de junio de 2026Se publica la versión 1.022 de septiembre de 2026Se presenta la 1.1; espera su vídeo de lanzamiento25 de septiembre de 2026La última prueba halla dos errores; ambos se corrigen ese día
- 27 de septiembre de 2026La 1.1.1 se envía a revisión de Apple30 de septiembre de 2026La 1.1.1 ya está en la Mac App Store

## La primera corrección: subtítulos que se montaban unos sobre otros

Al pulsar Analyze, la extensión transcribe por separado cada clip de diálogo de tu línea de tiempo y después une los resultados. En algunos proyectos, eso podía darte la misma frase dos veces o subtítulos montados unos sobre otros. Encontramos tres formas en que podía pasar:




- Un clip recortado. Recortas el inicio de un clip en la línea de tiempo, pero el habla de la parte oculta, recortada, aún podía aparecer como subtítulos.

- Dos clips con el mismo diálogo. Piensa en el audio de la cámara y un micrófono aparte, ambos marcados como diálogo. Las mismas palabras podían aparecer dos veces.

- El propio modelo de voz. A veces Whisper devuelve líneas que se solapan un poco.

Por sí solo, eso es molesto. Pero 1.1.1 también incluye un editor de subtítulos, y el editor hace algo sensato: rechaza cualquier cambio de tiempos que haga que un subtítulo se solape con el contiguo. Con duplicados que ya se solapaban, cualquier arreglo que probaras habría sido rechazado. Te habrías quedado sin salida, con un editor que parecía bloqueado.


Esto es lo que pasa ahora:




- Los subtítulos de cada clip se recortan a la parte del clip que realmente ves en la línea de tiempo, sin cortar palabras por la mitad.

- El habla duplicada se fusiona en un solo subtítulo.

- Cualquier solapamiento que quede se divide limpiamente.

- Los subtítulos guardados antes de la corrección se reparan automáticamente al cargarse.

Y hay un nuevo botón para eliminar en cada subtítulo. Si hay una línea que simplemente no quieres, bórrala. Seguirá borrada la próxima vez.



## La segunda corrección: audio que no estaba donde creíamos

Esta trata del audio que está separado de su vídeo o que va en un clip conectado. Un caso habitual es el sonido de una grabadora aparte, unido a tu clip principal.


En esos proyectos, la extensión podía leer mal las posiciones de tu línea de tiempo. En uno de nuestros proyectos de prueba, el audio separado era más largo que su vídeo. Solo se transcribió la duración del vídeo, y las dos fuentes estaban a 1,6 segundos de distancia. Los subtítulos se desincronizaban.


Ahora las posiciones de los clips anidados y conectados se calculan correctamente. Un clip conectado se mide en su propio argumento, en lugar de recortarse a la duración del clip del que cuelga. La imagen de un clip de vídeo ya no se confunde con una fuente de audio. Y se respetan los roles de audio, los clips desactivados y los canales de audio apagados.


Las dos correcciones vinieron del mismo sitio: los proyectos reales. Nos alegra haber probado con ellos una vez más.



## Smart Cache: no empieces de cero

Smart Cache recuerda, en tu Mac, lo que ya se ha transcrito.


Imagina esto. Subtitulas una entrevista y el resultado te convence. Entonces el cliente pide diez segundos más al final. Alargas el clip en la línea de tiempo y vuelves a pulsar Analyze. Solo la parte nueva, aún sin transcribir, pasa por Whisper. El resto ya está ahí.


Procesa el mismo clip otra vez, con el mismo idioma y el mismo modelo, y los subtítulos vuelven al instante. Eso ayuda mientras un montaje sigue cambiando: prueba otro estilo, vuelve a procesar, recorta, alarga, sin empezar de cero la pasada de subtítulos.


Smart Cache viene activado de forma predeterminada. Hay un interruptor en la extensión por si prefieres desactivarlo. La primera pasada de un clip sigue tardando lo que tarda, y eso depende de tu Mac, de tu clip y del modelo. Smart Cache ayuda en la segunda pasada, no en la primera.



## Corrige un subtítulo antes de que llegue a la línea de tiempo

Incluso un buen modelo de voz puede escribir el nombre de tu invitado a su manera. Ahora puedes corregir un nombre, un signo de puntuación o una frase entera dentro de la extensión, antes de que los títulos lleguen a la línea de tiempo.


También puedes cambiar el tiempo de inicio y de fin de cada subtítulo. El editor comprueba los tiempos sobre la marcha. Rechaza un intervalo no válido y un subtítulo que se solape con el contiguo, para que un cambio pequeño no rompa la secuencia sin que te des cuenta.


Tus cambios se guardan en tu Mac. Vuelven cuando abres de nuevo la extensión o cuando analizas el mismo material otra vez. Y, como novedad de 1.1.1, puedes eliminar un subtítulo que no quieras.



## Smart Search: ¿dónde dije eso?

Recuerdas haber dicho algo sobre un objetivo, pero no en qué vídeo. Smart Search recorre todos los subtítulos que has generado, en todos tus clips. Cada resultado muestra el texto coincidente, el nombre del archivo y el código de tiempo.


La búsqueda también ve tus correcciones. Si corregiste un nombre, el nombre corregido es el que puedes encontrar.


Un límite sincero: al hacer clic en un resultado no se salta al clip en Final Cut Pro. Obtienes el nombre del archivo y el código de tiempo, y llegas hasta allí por tu cuenta.



## Unos 100 idiomas y Auto Detect

La versión 1.0 tenía un selector con 20 idiomas. El menú de idiomas ahora muestra los aproximadamente 100 idiomas del catálogo del modelo Whisper. Arriba del todo hay una opción nueva, Auto Detect. Si no sabes con certeza qué idioma hay en un clip, o mezclas idiomas entre clips, deja que lo decida. Auto Detect también funciona en tu Mac, tras la descarga del modelo.


Lee esta parte con atención. Esa cifra es la cobertura de idiomas del modelo. No probamos la calidad de los subtítulos por separado en cada idioma. La precisión de los subtítulos depende del idioma, la grabación, el hablante y el modelo. Así que revisar tus subtítulos sigue siendo parte del trabajo, en cualquier idioma. Con el nuevo editor, además, es más rápido.



## Ventanas más pequeñas

La extensión ahora se adapta a ventanas más pequeñas de Final Cut Pro, por ejemplo en la pantalla de un portátil. La zona de arrastre del proyecto, la búsqueda y las plantillas siguen al alcance.



## Lo que no cambia



- La transcripción sigue ejecutándose en tu Mac. Usamos WhisperKit, que está basado en Whisper de OpenAI. Tu material no se sube a un servicio de transcripción en la nube. El modelo de voz se descarga una vez, y eso requiere internet. Las compras en el App Store y las comprobaciones de suscripción también usan internet.

- Las mismas cinco plantillas. Basic, Highlighted, Highlighted with Background, Pop y Beast Pop. La tipografía, el color y la posición siguen siendo ajustables.

- El mismo resultado ordenado. Tus títulos vuelven agrupados en un clip compuesto dentro de un argumento secundario.

- El mismo modelo de precios. La app se descarga gratis y las plantillas son gratuitas. Los subtítulos automáticos con IA requieren una suscripción mensual activa. Para ver los precios vigentes, consulta la [página del Mac App Store](https://apps.apple.com/app/id6775619373).


## Lo que no incluye esta actualización

Para que no te queden dudas: 1.1.1 no tiene exportación de SRT ni de otros archivos de subtítulos, ni síntesis de voz, ni subida automática a YouTube. La búsqueda encuentra palabras, no imágenes ni ideas, así que no hay búsqueda visual ni semántica. Y, como dijimos antes, un resultado de búsqueda no salta al clip.


Ya estamos trabajando en la próxima actualización. No prometeremos nada sobre ella aquí. Preferimos contártelo cuando esté lista.



## Descárgala, mira el vídeo y cuéntanos qué opinas

Para actualizar, abre el [Mac App Store](https://apps.apple.com/app/id6775619373) e instala FCP AI-Toolkit 1.1.1. La página del App Store ya está disponible en 10 idiomas y tiene un breve vídeo de vista previa.


Para verlo en acción, mira el [vídeo de lanzamiento en YouTube](https://www.youtube.com/watch?v=ZvGX2RwCvH8). Nuestros primeros vídeos, uno de lanzamiento y varios Shorts, están en [YouTube](https://www.youtube.com/@FCPAIToolkit) y en [Instagram](https://www.instagram.com/fcpaitoolkit/) como Reels. También estamos en [TikTok](https://www.tiktok.com/@fcpaitoolkit). Si quieres leer cómo hemos llegado hasta aquí, la [publicación de 1.0](/es/blog/fcp-ai-toolkit-1-0/) y el [avance de 1.1](/es/blog/fcp-ai-toolkit-1-1-preview/) siguen en línea.


Si algo no funciona en tu proyecto, o tienes una idea, escríbenos a help@fcp-aitoolkit.com. Un proyecto real con un problema real es la mejor prueba que podemos tener. Así encontramos estos dos errores.


Gracias por usar FCP AI-Toolkit.
