from dataclasses import dataclass

import numpy as np

from app.volumes.mesh import TriangleMesh, extract_mesh
from app.volumes.sampling import SampledGrid, sample_function


@dataclass(frozen=True)
class VolumeEstimate:
    voxel_volume: float
    mesh_volume: float
    domain_volume: float


def voxel_volume(grid: SampledGrid) -> float:
    cell_volume = float(np.prod(grid.spacing))
    return float(np.count_nonzero(grid.values <= 0)) * cell_volume


def mesh_volume(mesh: TriangleMesh) -> float:
    """Volumen encerrado por una malla cerrada (teorema de la divergencia, tetraedros con el origen)."""
    if mesh.is_empty:
        return 0.0
    v0, v1, v2 = (mesh.vertices[mesh.faces[:, i]] for i in range(3))
    signed = np.einsum("ij,ij->i", v0, np.cross(v1, v2)).sum() / 6.0
    # La suma de tetraedros acumula error de redondeo y el signo depende de la orientación
    # numérica de los triángulos; el volumen es una magnitud, se reporta en valor absoluto.
    return float(abs(signed))


def domain_volume(domain: list[list[float]]) -> float:
    return float(np.prod([upper - lower for lower, upper in domain]))


def estimate_volume(expression: str, domain: list[list[float]], resolution: int) -> VolumeEstimate:
    grid = sample_function(expression, domain, resolution)
    return VolumeEstimate(
        voxel_volume=voxel_volume(grid),
        mesh_volume=mesh_volume(extract_mesh(grid)),
        domain_volume=domain_volume(domain),
    )
