from typing import List, TYPE_CHECKING

from app.database.schemas import CandidateResponse

if TYPE_CHECKING:
    from app.position.repositories.position_repository import PositionRepository


class PositionService:
    def __init__(self, position_repository: "PositionRepository") -> None:
        self.position_repository = position_repository

    async def get_positions(self):
        results = await self.position_repository.get_open_positions_with_details()

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
