from fastapi import APIRouter

from app.core.logging import get_logger
from app.core.time import now_formatted
from app.functions.dependencies import OwnedFunction
from app.volumes.schemas import VolumeResult
from app.volumes.volume import estimate_volume

router = APIRouter(prefix="/functions", tags=["volumes"])
logger = get_logger(__name__)


@router.get("/{function_id}/volume")
def get_volume(function: OwnedFunction) -> VolumeResult:
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
