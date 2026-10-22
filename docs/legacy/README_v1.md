# Prueba de desarrollador backend con FastAPI

En esta prueba, se debe crear una aplicación web utilizando FastAPI que consuma datos de la API pública <https://jsonplaceholder.typicode.com/guide> y cumpla con los requisitos detallados a continuación.

## Objetivo de la prueba

El objetivo de esta prueba es evaluar las habilidades en el desarrollo de aplicaciones backend con Python y FastAPI; se espera que el candidato desarrolle diferentes endpoints que consuman datos de la API de JSONPlaceholder, se comuniquen entre sí y manejen adecuadamente la información adicional y los registros (logs).

## Metodología a utilizar

Se debe utilizar FastAPI como framework para crear la aplicación web; además, se recomienda seguir las buenas prácticas de desarrollo, como la utilización de versiones controladas de Python (por ejemplo, utilizando Pyenv o pyenv-virtualenv), el uso de un gestor de dependencias (por ejemplo, pipenv o poetry) y la escritura de tests unitarios para tus endpoints.

## Entregables

Los entregables de esta prueba son:

1. Un fork de este repositorio que contenga el código fuente.
2. Un archivo README.md dentro del repositorio con una breve descripción del proyecto, cómo ejecutar la aplicación y cualquier otra información relevante.
3. Para la entrega se debe realizar una presentación de no mas de 30 minutos 15 minutos de preguntas donde se explique el uso de la aplicación y también una breve exposición de la educación y experiencia del candidato.

## Endpoints a implementar

Se deben crear al menos los siguientes dos endpoints que se comuniquen entre sí:

1. Un endpoint `/users/{id}` que devuelva información detallada de un usuario específico de la API de JSONPlaceholder; además, deberás incluir información adicional como la fecha y hora actual en el formato `YYYY-MM-DD HH:MM:SS` y registrar (log) cualquier error que ocurra durante la obtención de los datos.
2. Un endpoint `/posts` que devuelva una lista de publicaciones de la API de JSONPlaceholder; para este endpoint, se debe filtrar las publicaciones por usuario utilizando el `id` del usuario obtenido en el primer endpoint; también se debe incluir información adicional como la fecha y hora actual en el formato `YYYY-MM-DD HH:MM:SS` y registrar (log) cualquier error que ocurra durante la obtención de los datos.


