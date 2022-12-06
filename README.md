# Charlas con chatGPT

Compilación de charlas exploratorias con ChatGPT (https://chat.openai.com/).

Los HTML originales fueron obtenidos con las herramientas de desarrollador del browser.
Que posteriormente fueron reprocesados (para eliminar tags innecesarios y de interfaz) mediante el script "./utiles/actualizar.py".

En ese postprocesado se le agregaron datos extras, como flechas y elementos para facilitar la navegación y adaptar la estética.

El contenido puede navegarse en https://caalma.github.io/charlas_con_chatgpt/.

## ¿Cómo obtener el html crudo de las charlas?
Actualmente uso las Herramientas de Desarrollador disponibles en el navedador de internet.
Una vez realizada la charla, hacer los siguientes pasos:
1 - Click derecho sobre cualquier parte del html. Elegir la opción "Inspeccionar".
2 - En el árbol de elementos, hacer click izquierdo sobre el tag `<html>`, para seleccionarlo.
3 - Click derecho sobre el mismo tag. Elegir del menu contextual `Copiar` y luego `Copiar outerHTML`.
4 - Pegar el contenido en cualquier editor de texto y grabarlo en la carpeta `./base/charlas_nuevas/`.
