from dataclasses import dataclass

import numpy as np

from app.functions.parser import FloatArray, compile_expression

Vector3 = tuple[float, float, float]


@dataclass(frozen=True)
class SampledGrid:
    """Valores de f en una rejilla regular; ``values[i, j, k]`` corresponde a (x_i, y_j, z_k)."""

    values: FloatArray
    origin: Vector3
    spacing: Vector3

    @property
    def shape(self) -> tuple[int, int, int]:
        nx, ny, nz = self.values.shape
        return nx, ny, nz


def build_axes(domain: list[list[float]], resolution: int) -> list[FloatArray]:
    return [np.linspace(lower, upper, resolution) for lower, upper in domain]


def sample_function(expression: str, domain: list[list[float]], resolution: int) -> SampledGrid:
    axes = build_axes(domain, resolution)
    # Indexado cartesiano: mismo convenio de ejes que el visor (three.js, X derecha / Y arriba).
    x, y, z = np.meshgrid(*axes, indexing="xy")
    values = compile_expression(expression)(x, y, z)

    origin = (float(axes[0][0]), float(axes[1][0]), float(axes[2][0]))
    spacing = (
        float(axes[0][1] - axes[0][0]),
        float(axes[1][1] - axes[1][0]),
        float(axes[2][1] - axes[2][0]),
    )
    return SampledGrid(values=values, origin=origin, spacing=spacing)
