from fastapi import HTTPException
from typing import List, TYPE_CHECKING

from app.database.schemas import (
    CandidateResponse,
    PositionUpdate,
    PositionUpdateResponse,
)

if TYPE_CHECKING:
    from app.position.repositories.position_repository import PositionRepository


class PositionService:
    def __init__(self, position_repository: "PositionRepository") -> None:
        self.position_repository = position_repository

    async def get_positions(self):
        results = await self.position_repository.get_open_positions_with_details()
        print(results)
        open_positions_with_details = []
        for open_position, project, soft_skill_ids, technology_ids in results:
            open_positions_with_details.append(
                {
                    "open_position": open_position,
                    "project": project,
                    "soft_skill_ids": soft_skill_ids,
                    "technology_ids": technology_ids,
                }
            )
        return open_positions_with_details

    async def get_position_candidates(
        self, position_id: int
    ) -> List[CandidateResponse]:
        candidates = await self.position_repository.get_open_position_candidates(
            position_id
        )
        candidates_output = []
        for candidate in candidates:
            candidates_output.append(
                {
                    "candidate_id": candidate.candidate_id,
                    "technical_score": candidate.technical_score,
                    "softskill_score": candidate.softskill_score,
                    "general_score": candidate.general_score,
                }
            )

        return candidates_output

    async def update_position_chosen_candidate(
        self, position_id: int, position_data: PositionUpdate
    ) -> PositionUpdateResponse:
        candidates = await self.position_repository.get_open_position_candidates(
            position_id
        )
        not_candidate_for_pos = True
        for candidate in candidates:
            if candidate.candidate_id == position_data.candidate_id:
                not_candidate_for_pos = False
        if not_candidate_for_pos:
            raise HTTPException(
                412,
                "Candidato no hace parte de proceso de selección de posición indicada",
            )
        updated_position = await self.position_repository.update_open_position(
            position_id, position_data.candidate_id
        )
        positions = await self.position_repository.get_project_positions(
            updated_position.project_id
        )
        is_project_closed = True
        for position in positions:
            if position.is_open:
                is_project_closed = False
        if is_project_closed:
            await self.position_repository.close_project(updated_position.project_id)
        return PositionUpdateResponse.model_validate(
            {
                "id": updated_position.id,
                "project_id": updated_position.project_id,
                "is_open": updated_position.is_open,
                "candidate_id": updated_position.candidate_id,
            }
        )
