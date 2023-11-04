from typing import List, TYPE_CHECKING
from fastapi import APIRouter

from app.database.schemas import (
    CandidateResponse,
    PositionUpdate,
    PositionUpdateResponse,
)

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

    @router.patch("/{position_id}")
    async def update_position_chosen_candidate(
        position_id: int, position: PositionUpdate
    ) -> PositionUpdateResponse:
        return await position_service.update_position_chosen_candidate(
            position_id, position
        )

    return {
        "get_positions": get_positions,
        "get_position_candidates": get_position_candidates,
        "update_position_chosen_candidate": update_position_chosen_candidate,
    }
