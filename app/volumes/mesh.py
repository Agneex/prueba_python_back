from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from skimage.measure import marching_cubes

from app.functions.parser import FloatArray
from app.volumes.sampling import SampledGrid

ISO_LEVEL = 0.0
# Valor positivo (exterior) con el que se rodea la rejilla para cerrar la superficie en los bordes.
OUTSIDE_PAD_VALUE = 1.0


@dataclass(frozen=True)
class TriangleMesh:
    vertices: FloatArray
    faces: NDArray[np.int64]

    @property
    def is_empty(self) -> bool:
        return len(self.faces) == 0


def extract_mesh(grid: SampledGrid) -> TriangleMesh:
    """Extrae la superficie f = 0 con marching cubes, cerrada contra los bordes del dominio."""
    values = grid.values
    if values.min() > ISO_LEVEL or values.max() < ISO_LEVEL:
        return TriangleMesh(vertices=np.empty((0, 3)), faces=np.empty((0, 3), dtype=np.int64))

    padded = np.pad(values, 1, mode="constant", constant_values=OUTSIDE_PAD_VALUE)
    # f < 0 en el interior: "descent" orienta las normales hacia el exterior.
    vertices, faces, _, _ = marching_cubes(
        padded, level=ISO_LEVEL, spacing=grid.spacing, gradient_direction="descent"
    )
    vertices += np.asarray(grid.origin) - np.asarray(grid.spacing)
    return TriangleMesh(vertices=vertices, faces=faces.astype(np.int64))
