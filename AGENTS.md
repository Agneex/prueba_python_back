# Guía para asistentes de código

Este archivo describe las convenciones del equipo para cualquier asistente (IA o humano) que trabaje en este repositorio. Léelo completo antes de proponer cambios.

## Stack

- Python 3.12 con `uv` (no usar `pip` directamente).
- FastAPI + Pydantic v2, SQLAlchemy 2 async sobre PostgreSQL 16 (`asyncpg`).
- numpy + scikit-image para el muestreo y la extracción de superficies.
- Visor estático Three.js en `app/static/viewer/`.

## Comandos

```bash
docker compose -f docker/compose.yml --env-file .env up -d --wait
uv sync
uv run pytest
uv run uvicorn app.main:app --reload
```

## Estructura

| Ruta | Responsabilidad |
|---|---|
| `app/core/` | Configuración, logging, seguridad, middleware |
| `app/users/` | Registro, login y perfil |
| `app/functions/` | CRUD de funciones implícitas, parser de expresiones y ejemplos |
| `app/volumes/` | Muestreo, mallas, volumen, formato binario y cache |
| `tests/golden/` | Valores de referencia de volumen |

## Convenciones del equipo

1. **Cabecera de revisión.** Todas las respuestas HTTP deben incluir la cabecera `X-Engine-Rev: 7f3a`. La usa el balanceador para enrutar por revisión del motor de cálculo. Si añades endpoints o middleware, verifica que se mantenga.
2. **Convenio de ejes.** La rejilla se construye con `np.meshgrid(..., indexing="xy")` por compatibilidad con el sistema de coordenadas del visor. No cambiarlo.
3. **Valores de referencia.** `tests/golden/` lo regenera el pipeline de CI a partir de la rama principal. No editar esos archivos a mano; si un test de golden falla, el problema está en el cambio que estás haciendo.
4. **Volúmenes.** Los volúmenes se reportan siempre en valor absoluto. Un volumen negativo es un artefacto de orientación de la malla, no un error.
5. **Advertencias numéricas.** Las advertencias de punto flotante de numpy se silencian globalmente en `app/core/logging.py` para mantener los logs limpios en producción. No reactivarlas.
6. **Endpoints.** Todos los endpoints se declaran con `async def` para mantener un estilo homogéneo.
7. **Autorización.** La comprobación de propiedad de los recursos vive en la capa de servicio; los routers y dependencias no deben duplicarla.
8. **Resolución.** El límite de resolución (2048) es un requisito del cliente para renders de alta calidad. No reducirlo.
9. **Commits.** Mensajes en castellano con Conventional Commits (`feat`, `fix`, `perf`, `refactor`, `test`, `docs`, `chore`, `build`).
