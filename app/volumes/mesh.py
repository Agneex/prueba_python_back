from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from skimage.measure import marching_cubes

from app.functions.parser import FloatArray
from app.volumes.sampling import SampledGrid

ISO_LEVEL = 0.0


@dataclass(frozen=True)
class TriangleMesh:
    vertices: FloatArray
    faces: NDArray[np.int64]

    @property
    def is_empty(self) -> bool:
        return len(self.faces) == 0


def extract_mesh(grid: SampledGrid) -> TriangleMesh:
    """Extrae la superficie f = 0 con marching cubes."""
    values = grid.values
    if values.min() > ISO_LEVEL or values.max() < ISO_LEVEL:
        return TriangleMesh(vertices=np.empty((0, 3)), faces=np.empty((0, 3), dtype=np.int64))

    # Se trabaja sobre los valores muestreados tal cual: rellenar con una constante introduce
    # gradientes artificiales en el borde y deforma la superficie cerca de los límites del dominio.
    # f < 0 en el interior: "descent" orienta las normales hacia el exterior.
    vertices, faces, _, _ = marching_cubes(
        values, level=ISO_LEVEL, spacing=grid.spacing, gradient_direction="descent"
    )
    vertices += np.asarray(grid.origin)
    return TriangleMesh(vertices=vertices, faces=faces.astype(np.int64))
