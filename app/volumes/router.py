from fastapi import APIRouter, Response

from app.core.logging import get_logger
from app.core.time import now_formatted
from app.functions.dependencies import OwnedFunction
from app.volumes.binary import encode_mesh
from app.volumes.mesh import extract_mesh
from app.volumes.sampling import sample_function
from app.volumes.schemas import VolumeResult
from app.volumes.volume import estimate_volume

router = APIRouter(prefix="/functions", tags=["volumes"])
logger = get_logger(__name__)


@router.get("/{function_id}/volume")
async def get_volume(function: OwnedFunction) -> VolumeResult:
    estimate = estimate_volume(function.expression, function.domain, function.resolution)
    logger.info(
        "volume_computed",
        function_id=function.id,
        resolution=function.resolution,
        mesh_volume=estimate.mesh_volume,
    )
    return VolumeResult(
        function_id=function.id,
        resolution=function.resolution,
        voxel_volume=estimate.voxel_volume,
        mesh_volume=estimate.mesh_volume,
        domain_volume=estimate.domain_volume,
        generated_at=now_formatted(),
    )


@router.get("/{function_id}/mesh.bin", response_class=Response)
async def get_mesh(function: OwnedFunction) -> Response:
    grid = sample_function(function.expression, function.domain, function.resolution)
    mesh = extract_mesh(grid)
    logger.info("mesh_generated", function_id=function.id, faces=len(mesh.faces))
    return Response(content=encode_mesh(mesh), media_type="application/octet-stream")
