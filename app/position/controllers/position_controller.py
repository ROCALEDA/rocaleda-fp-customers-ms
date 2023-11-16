from typing import List, TYPE_CHECKING
from fastapi import APIRouter

from app.database.schemas import (
    CandidateResponse,
    PerformanceEvaluationCreation,
    PositionUpdate,
    PositionUpdateResponse,
    TechnicalTestResponse,
    TechnicalTestResults,
)

if TYPE_CHECKING:  # pragma: no cover
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

    @router.get("/closed/{project_id}")
    async def get_closed_positions_by_project_id(project_id: int):
        return await position_service.get_closed_positions_by_project_id(project_id)

    @router.post("/evaluations")
    async def create_position_evaluation(evaluation: PerformanceEvaluationCreation):
        return await position_service.create_position_evaluation(evaluation)

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

    @router.post("/{position_id}/tests")
    async def save_technical_test_result(
        position_id: int, test_results: TechnicalTestResults
    ) -> TechnicalTestResponse:
        return await position_service.save_technical_test_result(
            position_id, test_results
        )

    return {
        "get_positions": get_positions,
        "get_position_candidates": get_position_candidates,
        "update_position_chosen_candidate": update_position_chosen_candidate,
        "get_closed_positions_by_project_id": get_closed_positions_by_project_id,
        "create_position_evaluation": create_position_evaluation,
        "save_technical_test_result": save_technical_test_result,
    }
