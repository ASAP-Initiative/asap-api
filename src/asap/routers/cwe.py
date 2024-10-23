from fastapi import APIRouter, HTTPException

from asap.db.models.cwe import CWE, cwe_by_id, cwe_list

router = APIRouter(
    tags=["cwe"]
)

@router.get("/cwe")
def list_cwe() -> list[CWE]:
    return cwe_list()


@router.get("/cwe/{cwe_id}")
def get_cwe(cwe_id: str):# -> CWE | None:
    return cwe_by_id(cwe_id)
