# Guía de contribución

## Puesta en marcha

Las instrucciones para levantar el proyecto están en el [`README.md`](README.md).

## Flujo de trabajo

1. Crea una rama a partir de `main` con un nombre que describa el cambio (por ejemplo, `feature/filtro-por-usuario`).
2. Haz commits pequeños y atómicos: cada uno debe tener un propósito claro y dejar el proyecto en un estado que funcione.
3. Ejecuta las pruebas antes de abrir el pull request:
   ```bash
   uv run pytest
   ```
4. Abre un pull request usando la plantilla y espera la revisión de al menos una persona del equipo.

## Mensajes de commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/es/) en castellano:

| Tipo | Uso |
|---|---|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de un error |
| `perf` | Mejora de rendimiento |
| `refactor` | Cambio interno sin modificar el comportamiento |
| `test` | Añadir o corregir pruebas |
| `docs` | Documentación |
| `build`, `ci`, `chore` | Herramientas, integración continua y tareas de mantenimiento |

El asunto debe describir con precisión el cambio y quedar en una sola línea.

## Estilo de código

- Python 3.12 con tipado en las firmas públicas.
- La configuración de `ruff` está en `pyproject.toml`.
- Las variables configurables se leen del entorno; no dejes valores escritos en el código.
