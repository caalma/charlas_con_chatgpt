# Charlas con chatGPT

Compilación de charlas exploratorias con ChatGPT (https://chat.openai.com/).

El contenido puede navegarse en https://caalma.github.io/charlas_con_chatgpt/.

## ¿Cómo obtener el html crudo de las charlas?

Actualmente uso las Herramientas de Desarrollador disponibles en el navedador de internet.
Una vez realizada la charla, hacer los siguientes pasos:
1. Click derecho sobre cualquier parte del html. Elegir la opción "Inspeccionar".
2. En el árbol de elementos, hacer click izquierdo sobre el tag `<html>`, para seleccionarlo.
3. Click derecho sobre el mismo tag. Elegir del menu contextual `Copiar` y luego `Copiar outerHTML`.
4. Pegar el contenido en cualquier editor de texto y grabarlo en la carpeta `./base/charlas_nuevas/`. El archivo deberá tener extensión `.html`.

## ¿Cómo post-procesar las charlas?

El postprocesado se realiza para eliminar tags innecesarios y de interfaz. Además se le agregaron datos extras como flechas y elementos para facilitar la navegación y adaptar la estética.

Se realizan ejecutando `./utiles/actualizar.py`, de la siguiente forma:
1. `./actualizar.py agregar`: incorpora las charlas nuevas a la carpeta `charlas_crudas` y almacenar una referencia de la fecha de creación de la charla en `./base/registro_temporal.yml`.
2. `./actualizar.py publicar_nuevos`: postprocesa y publica las charlas agregadas en `./docs/charlas/`.
3. `./actualizar.py indice`: actualiza el archivo `./docs/index.html` con los enlaces a las nuevas charlas.
4. `./actualizar.py notas`: actualiza el archivo `./docs/notas.html` con el contenido de `./base/notas.yml`.

## ¿Cómo ver en un server local el contenido generado?

Ejecutando `./utiles/server_local.py`


## Salvedades

+ El uso de los script requiere cumplir los requerimientos indicados en `./utiles/README.md`.
+ La estructura de los html crudo, está siendo actualizada por los desarrolladores de ChatGPT. Con lo cual es posible que al postprocesar futuras charlas no se obtenga el resultado final esperado. Al día de hoy (2022-12-06) están disponibles 2 modelos de filtrado.
