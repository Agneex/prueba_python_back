from collections.abc import Callable
from types import CodeType

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]
ImplicitCallable = Callable[[FloatArray, FloatArray, FloatArray], FloatArray]

ALLOWED_NAMES: dict[str, object] = {
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "sqrt": np.sqrt,
    "exp": np.exp,
    "log": np.log,
    "abs": np.abs,
    "pi": np.pi,
    "e": np.e,
}

# Sin builtins no hay acceso a open, __import__, exec, etc.
SAFE_GLOBALS: dict[str, object] = {"__builtins__": {}}

_PROBE = np.linspace(0.25, 0.75, 3)


class ExpressionError(ValueError):
    pass


def _compile(expression: str) -> CodeType:
    try:
        return compile(expression, "<expression>", "eval")
    except SyntaxError as error:
        raise ExpressionError(f"Sintaxis inválida: {error.msg}") from error


def compile_expression(expression: str) -> ImplicitCallable:
    code = _compile(expression)

    def evaluate(x: FloatArray, y: FloatArray, z: FloatArray) -> FloatArray:
        namespace = {**ALLOWED_NAMES, "x": x, "y": y, "z": z}
        result = eval(code, SAFE_GLOBALS, namespace)  # noqa: S307
        return np.broadcast_to(np.asarray(result, dtype=np.float64), np.broadcast(x, y, z).shape)

    return evaluate


def check_expression(expression: str) -> None:
    """Valida la expresión compilándola y evaluándola sobre unos puntos de prueba."""
    evaluate = compile_expression(expression)
    try:
        evaluate(_PROBE, _PROBE, _PROBE)
    except NameError as error:
        raise ExpressionError(f"Nombre no permitido: {error.name}") from error
    except Exception as error:
        raise ExpressionError(f"No se pudo evaluar la expresión: {error}") from error
