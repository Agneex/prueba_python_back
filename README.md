# Prueba de desarrollador backend con FastAPI

En esta prueba, se debe crear una aplicación utilizando FastAPI que consuma datos de la API pública <https://jsonplaceholder.typicode.com/guide> y cumpla con los requisitos detallados a continuación.

## Objetivo de la prueba
El objetivo de esta prueba es evaluar las habilidades técnicas en el desarrollo de aplicaciones backend utilizando Python y el framework FastAPI , incluyendo:

* Consumo de APIs externas (en este caso, JSONPlaceholder ).
* Manejo de solicitudes HTTP asíncronas o síncronas.
* Separación de responsabilidades (lógica de negocio, servicios, controladores).
* Manejo de errores y logging.
* Buenas prácticas de código: legibilidad, documentación, testing (opcional).

## Metodología a utilizar

* Utiliza FastAPI como framework principal.
* Usa un entorno virtual gestionado con pyenv + venv , pipenv o poetry .
* Escribe al menos dos endpoints RESTful que cumplan con los requisitos especificados.
* Incluye tests unitarios (opcional, pero valorado positivamente).
* Documenta tu proyecto usando OpenAPI/Swagger (ya integrado en FastAPI) y un buen README.md.
* Implementa logging para registrar errores y eventos importantes.
* Usa buenas prácticas de programación: funciones reutilizables, comentarios claros, etc.

## Entregables

Los entregables de esta prueba son:

1. Un **fork de este repositorio** con el código fuente del proyecto.
2. Un archivo README.md con:
    * Una breve descripción del proyecto.
    * Instrucciones detalladas para ejecutar la aplicación (instalación de dependencias, levantar servidor, etc.).
    * Ejemplos de uso de los endpoints (pueden incluir curl, Postman o Swagger UI).
    * Opcional: instrucciones para correr tests.
3. Una presentación de máximo 30 minutos , incluyendo:
    * Demostración funcional de la aplicación.
    * Explicación de tu enfoque técnico y decisiones de diseño.
    * Breve exposición sobre tu formación y experiencia profesional (máximo 15 minutos).

## Endpoints a implementar

Se deben crear al menos los siguientes dos endpoints que se comuniquen entre sí:

1. Un endpoint `/users/{id}` que devuelva información detallada de un usuario específico de la API de JSONPlaceholder; además, deberás incluir información adicional como la fecha y hora actual en el formato `YYYY-MM-DD HH:MM:SS` y registrar (log) cualquier error que ocurra durante la obtención de los datos.
2. Un endpoint `/posts` que devuelva una lista de publicaciones de la API de JSONPlaceholder; para este endpoint, se debe filtrar las publicaciones por usuario utilizando el `id` del usuario obtenido en el primer endpoint; también se debe incluir información adicional como la fecha y hora actual en el formato `YYYY-MM-DD HH:MM:SS` y registrar (log) cualquier error que ocurra durante la obtención de los datos.

## Puntos extra (opcionales)
* Implementar Dockerización del proyecto.
* Documentar el proyecto con Sphinx o MkDocs.
* Publicar una imagen de Docker en Docker Hub (si aplica).
* Implementar validación de modelos con Pydantic.

