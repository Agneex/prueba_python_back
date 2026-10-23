import numpy as np
import pytest

from app.functions.parser import ExpressionError, check_expression, compile_expression


def test_compiled_expression_evaluates_arrays():
    evaluate = compile_expression("x**2 + y**2 + z**2 - 1")
    values = evaluate(np.array([0.0, 1.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))

    np.testing.assert_allclose(values, [-1.0, 0.0])


def test_constant_expression_is_broadcast():
    evaluate = compile_expression("pi")
    values = evaluate(np.zeros(4), np.zeros(4), np.zeros(4))

    assert values.shape == (4,)


@pytest.mark.parametrize("expression", ["sin(x) * cos(y) + z", "sqrt(x**2 + y**2) - 0.5", "exp(-x) - e"])
def test_check_accepts_allowed_functions(expression):
    check_expression(expression)


@pytest.mark.parametrize("expression", ["x +* y", "open('/etc/passwd')", "__import__('os')", "foo(x)"])
def test_check_rejects_invalid_expressions(expression):
    with pytest.raises(ExpressionError):
        check_expression(expression)
