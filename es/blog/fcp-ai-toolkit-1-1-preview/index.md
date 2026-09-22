# Próximamente en 1.1: menos repeticiones, más control.

Date: 2026-09-22
Status: Próximamente
Language: es
Canonical: https://www.fcp-aitoolkit.com/es/blog/fcp-ai-toolkit-1-1-preview/

Smart Cache, correcciones de subtítulos persistentes, búsqueda en transcripciones y 100 idiomas del modelo Whisper con Auto Detect. Esto es lo que estamos preparando.

La versión 1.1 llegará pronto. Esta actualización se centra en lo que ocurre cuando retomas un montaje: volver a procesar el mismo audio, corregir un subtítulo, ajustar sus tiempos o intentar encontrar una frase que recuerdas haber oído.

Estamos incorporando Smart Cache, edición persistente de subtítulos, Smart Search y un selector de idioma más completo a FCP AI-Toolkit. El lanzamiento se está preparando; la versión disponible en el Mac App Store sigue siendo la 1.0. Aún no hemos anunciado una fecha de lanzamiento para la 1.1.


## Transcribe una vez. Reutiliza el trabajo.
Smart Cache recordará en tu Mac las secciones del material que ya se hayan transcrito. Cuando vuelvas a analizar el mismo contenido con el mismo idioma y modelo, la extensión podrá reutilizar los resultados en vez de pedir al modelo que repita todo el trabajo.

Si alargas un clip para incluir audio que aún no se ha transcrito, solo habrá que transcribir los fragmentos que faltan. Esto resulta especialmente útil mientras el montaje sigue cambiando: podrás volver a un clip o probar otro estilo de título sin empezar de cero cada pasada de subtítulos. Smart Cache estará activado de forma predeterminada, con la opción de desactivarlo.


## Haz una corrección. Consérvala.
El nuevo editor permitirá cambiar el texto de los subtítulos directamente en la extensión. Corrige un nombre, ajusta la puntuación o retoca una frase antes de generar los títulos. Las correcciones se guardarán localmente y volverán a aplicarse cuando reutilices ese material almacenado en caché.

Los cambios en los tiempos de inicio y fin también se conservarán. Podrás afinar la sincronización de un subtítulo y mantener ese ajuste al volver a abrir la extensión o analizar de nuevo el material. El editor comprueba los intervalos de tiempo no válidos y los solapamientos entre subtítulos contiguos para que un pequeño cambio de tiempo no estropee la secuencia sin que lo adviertas.


## Encuentra esa frase que recuerdas
Smart Search permitirá buscar en los subtítulos guardados en tu caché local. Los resultados mostrarán el texto coincidente, el nombre del archivo de origen y el código de tiempo, para ayudarte a localizar una frase útil sin leer cada transcripción.

La búsqueda reflejará las correcciones de texto guardadas, de modo que podrás encontrar el nombre que hayas corregido en el editor. En 1.1, cada resultado de búsqueda ofrece una referencia al material y al momento correspondiente. Al hacer clic en un resultado no se abrirá directamente el clip en Final Cut Pro.


## 100 idiomas del modelo, más Auto Detect
El selector de idioma ofrecerá los 100 códigos de idioma del catálogo del modelo Whisper, junto con Auto Detect. Elige un idioma de forma explícita o deja que el modelo lo identifique localmente durante la transcripción. Una vez descargado el modelo, la transcripción y la detección del idioma permanecen en tu Mac.

Esta cifra describe la cobertura lingüística del modelo. No significa que hayamos probado por separado la calidad de la transcripción en cada idioma. La precisión sigue dependiendo del idioma, la grabación, el hablante y el modelo, así que revisar los subtítulos generados sigue formando parte del trabajo.


## El mismo flujo de títulos, con menos interrupciones
Las cinco plantillas de Motion existentes y la transferencia mediante FCPXML siguen formando parte de la experiencia. También estamos mejorando cómo se adapta la extensión a los tamaños de ventana guardados por Final Cut Pro, para que la zona de arrastre del proyecto y las opciones de plantillas sigan siendo accesibles en ventanas más pequeñas.

La distinción de precios no cambia: las plantillas de Motion son gratuitas y el flujo de subtítulos con IA requiere una suscripción mensual activa. La versión 1.1 se centra en la caché, la edición, la búsqueda y la cobertura de idiomas. La exportación SRT, la síntesis de voz y la búsqueda visual o semántica quedan fuera de esta actualización.

Publicaremos aquí el anuncio cuando la versión 1.1 esté disponible. Sigue nuestros canales de [YouTube](https://youtube.com/@fcpaitoolki?si=HdQzmtITilWRwaA-), [Instagram](https://www.instagram.com/fcpaitoolkit/) y [TikTok](https://www.tiktok.com/@fcpaitoolkit) para ver los próximos tutoriales y novedades a medida que empecemos a publicar.
