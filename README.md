# Prueba de desarrollador backend con FastAPI — v2

> La versión anterior del enunciado se conserva en [`docs/legacy/README_v1.md`](docs/legacy/README_v1.md) solo como referencia histórica.

En esta prueba trabajarás sobre una API existente, construida con FastAPI, que permite a usuarios autenticados registrar **funciones implícitas** `f(x, y, z)`, calcular el **volumen** de la región `f(x, y, z) ≤ 0` dentro de un dominio acotado y **visualizarla en 3D** en el navegador.

El repositorio ya contiene una implementación parcial. Tu trabajo consiste en completarla, corregirla y dejarla lista para producción.

## Objetivo de la prueba

Evaluar tu capacidad para:

- Leer, entender y razonar sobre código existente.
- Diseñar e implementar endpoints con FastAPI siguiendo buenas prácticas.
- Validar que los resultados que entrega tu código son correctos, no solo que el código "corre".
- Trabajar con Git de forma ordenada y profesional.

**Se permite el uso de asistentes de IA.** Sin embargo, eres responsable de cada línea que entregues. En la sustentación deberás explicar cualquier parte del código y cualquier commit de tu historial.

## Metodología

- Python 3.12 gestionado con [`uv`](https://docs.astral.sh/uv/).
- FastAPI + Pydantic v2.
- SQLite (asíncrono) como base de datos. No se requiere Docker.
- Toda configuración se lee de variables de entorno (ver `.env.example`). No se aceptan valores sensibles en el código.
- Tests con `pytest`.

## Conceptos

Una **función implícita** es una expresión en las variables `x`, `y`, `z`. La superficie `f(x, y, z) = 0` separa el espacio en dos regiones; nos interesa la región **interior**, `f(x, y, z) ≤ 0`.

Cada función se guarda con:

| Campo | Descripción |
|---|---|
| `name` | Nombre descriptivo |
| `expression` | Expresión en `x`, `y`, `z` (ver operadores permitidos) |
| `domain` | Caja `[[xmin, xmax], [ymin, ymax], [zmin, zmax]]` donde se evalúa |
| `resolution` | Número de muestras por eje de la rejilla regular |

### Operadores y funciones permitidos en `expression`

| Elemento | Permitido |
|---|---|
| Variables | `x`, `y`, `z` |
| Constantes | números reales, `pi`, `e` |
| Aritmética | `+`, `-`, `*`, `/`, `**` |
| Funciones | `sin`, `cos`, `tan`, `sqrt`, `exp`, `log`, `abs` |

Cualquier otra construcción debe ser rechazada.

### Ejemplos

| Nombre | Expresión | Dominio sugerido |
|---|---|---|
| Esfera | `x**2 + y**2 + z**2 - 1` | `[-1.5, 1.5]³` |
| Toro | `(sqrt(x**2 + y**2) - 1)**2 + z**2 - 0.25**2` | `[-1.5, 1.5]³` |
| Gyroide | `sin(x)*cos(y) + sin(y)*cos(z) + sin(z)*cos(x)` | `[0, 2*pi]³` |
| Esfera recíproca | `1 - 1/(x**2 + y**2 + z**2)` | `[-2, 2]³` |
| Rampa tangente | `tan(x) - z` | `[0, 3]³` |
| Hipérbola | `1/x - y` | `[-2, 2]³` |

## Endpoints

| Método y ruta | Descripción |
|---|---|
| `POST /auth/register` | Registro de usuario |
| `POST /auth/token` | Login; devuelve un JWT |
| `GET /users/{id}` | Información del usuario. Incluye `generated_at` con la fecha y hora actual en formato `YYYY-MM-DD HH:MM:SS` |
| `POST /functions` · `GET /functions` | Crear y listar **las funciones del usuario autenticado** |
| `GET /functions/{id}` · `PATCH /functions/{id}` | Consultar y editar una función propia |
| `GET /functions/{id}/evaluate?x=&y=&z=` | Valor de `f` en un punto |
| `GET /functions/{id}/volume` | Volumen de la región `f ≤ 0` dentro del dominio |
| `GET /functions/{id}/mesh.bin` | Malla triangular de la superficie `f = 0` en formato binario |
| `GET /viewer?fn={id}` | Visor 3D de la función |

## Requisitos generales

1. Un usuario **solo** puede ver, editar, evaluar y visualizar sus propias funciones.
2. Todo error debe registrarse con logs estructurados.
3. La API nunca debe responder `500` ante una expresión válida.
4. El servicio debe seguir respondiendo a otras peticiones mientras calcula volúmenes o mallas.
5. Los límites de recursos (por ejemplo, la resolución máxima) deben ser configurables por variables de entorno.

## Tareas

### A. Usuarios y autorización
Completa el registro, el login y `GET /users/{id}`. Garantiza el requisito general 1 y demuéstralo con tests.

### B. Expresiones
Asegura que solo se aceptan las expresiones descritas en «Operadores y funciones permitidos». Las expresiones inválidas deben responder `422` con un mensaje claro.

### C. Volumen
`GET /functions/{id}/volume` debe ser correcto. Incluye en tu README una **tabla de convergencia** con el error relativo frente al valor analítico para la esfera, el toro y el gyroide, usando resoluciones 32, 64, 128 y 256. Explica cómo obtuviste los valores de referencia.

### D. Malla y visor
La superficie debe verse correctamente en `/viewer` para todos los ejemplos, incluso cuando el dominio está lejos del origen (por ejemplo, `x ∈ [599999, 600001]`).

### E. Robustez y recursos
Cumple los requisitos generales 3, 4 y 5.

## Entregables

1. Un **fork** de este repositorio con tu solución.
2. **Una rama por tarea** (A–E), integrada a `develop` mediante Pull Request.
3. **Commits atómicos realizados manualmente.** No se aceptan entregas con un único commit ni con *squash* de todo el trabajo. Cada mensaje de commit debe describir con precisión su contenido.
4. Un `README.md` con:
   - Descripción del proyecto y cómo ejecutarlo y probarlo.
   - La tabla de convergencia de la tarea C.
5. **Sustentación** de 45 minutos:
   - 10 min de demostración.
   - 20 min de ejercicio práctico en vivo sobre tu propio código.
   - 15 min de preguntas sobre tu historial de commits.
