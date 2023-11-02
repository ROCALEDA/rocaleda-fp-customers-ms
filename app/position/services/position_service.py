from typing import TYPE_CHECKING

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
