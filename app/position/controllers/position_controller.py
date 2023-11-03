from typing import List, TYPE_CHECKING
from fastapi import APIRouter

from app.database.schemas import CandidateResponse

if TYPE_CHECKING:
    from app.position.services.position_service import PositionService

router = APIRouter(
    prefix="/positions",
    tags=["positions"],
    responses={404: {"description": "Not found"}},
)


def initialize(position_service: "PositionService"):
    @router.get("")
    async def get_positions():
        return await position_service.get_positions()

    @router.get("/{position_id}/candidates")
    async def get_position_candidates(position_id: int) -> List[CandidateResponse]:
        return await position_service.get_position_candidates(position_id)

    return {
        "get_positions": get_positions,
        "get_position_candidates": get_position_candidates,
    }
