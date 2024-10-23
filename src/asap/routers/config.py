from fastapi import APIRouter

from ..config import ASAP_Config, asap_config

router = APIRouter(
    tags=["config"]
)

@router.get("/config")
def get_config() -> ASAP_Config:
    print(asap_config.data_dir)
    return asap_config
