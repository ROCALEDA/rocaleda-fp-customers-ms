from app.database import models, database
from sqlalchemy import func


class PositionRepository:
    async def get_open_positions_with_details(self):
        with database.create_session() as db:
            results = (
                db.query(
                    models.OpenPosition,
                    models.Project,
                    func.array_agg(models.PositionSoftSkill.soft_skill_id),
                    func.array_agg(models.PositionTechnology.technology_id),
                )
                .join(
                    models.Project, models.OpenPosition.project_id == models.Project.id
                )
                .outerjoin(
                    models.PositionSoftSkill,
                    models.OpenPosition.id == models.PositionSoftSkill.open_position_id,
                )
                .outerjoin(
                    models.PositionTechnology,
                    models.OpenPosition.id
                    == models.PositionTechnology.open_position_id,
                )
                .group_by(models.OpenPosition.id, models.Project.id)
                .all()
            )

            return results
