from pydantic import BaseModel


class VolumeResult(BaseModel):
    function_id: int
    resolution: int
    voxel_volume: float
    mesh_volume: float
    domain_volume: float
    generated_at: str
