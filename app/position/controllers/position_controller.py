from typing import TYPE_CHECKING

from fastapi import APIRouter


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

    return {"get_positions": get_positions}
