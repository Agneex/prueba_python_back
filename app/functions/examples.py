from math import pi

from pydantic import BaseModel

from app.functions.schemas import FunctionCreate


class Example(BaseModel):
    slug: str
    function: FunctionCreate


def _cube(lower: float, upper: float) -> list[list[float]]:
    return [[lower, upper], [lower, upper], [lower, upper]]


EXAMPLES: list[Example] = [
    Example(
        slug="esfera",
        function=FunctionCreate(
            name="Esfera", expression="x**2 + y**2 + z**2 - 1", domain=_cube(-1.5, 1.5)
        ),
    ),
    Example(
        slug="toro",
        function=FunctionCreate(
            name="Toro",
            expression="(sqrt(x**2 + y**2) - 1)**2 + z**2 - 0.25**2",
            domain=_cube(-1.5, 1.5),
        ),
    ),
    Example(
        slug="gyroide",
        function=FunctionCreate(
            name="Gyroide",
            expression="sin(x)*cos(y) + sin(y)*cos(z) + sin(z)*cos(x)",
            domain=_cube(0, 2 * pi),
        ),
    ),
    Example(
        slug="esfera-reciproca",
        function=FunctionCreate(
            name="Esfera recíproca", expression="1 - 1/(x**2 + y**2 + z**2)", domain=_cube(-2, 2)
        ),
    ),
    Example(
        slug="rampa-tangente",
        function=FunctionCreate(name="Rampa tangente", expression="tan(x) - z", domain=_cube(0, 3)),
    ),
    Example(
        slug="hiperbola",
        function=FunctionCreate(name="Hipérbola", expression="1/x - y", domain=_cube(-2, 2)),
    ),
]

EXAMPLES_BY_SLUG = {example.slug: example for example in EXAMPLES}
