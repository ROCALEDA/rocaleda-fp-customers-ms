from datetime import datetime
from app.database import models, database
from sqlalchemy import func

from app.database.schemas import PerformanceEvaluationCreation, TechnicalTestResults


class PositionRepository:
    async def get_closed_positions_by_project_id(self, project_id: int):
        with database.create_session() as db:
            return (
                db.query(models.OpenPosition)
                .filter(
                    models.OpenPosition.project_id == project_id,
                    models.OpenPosition.candidate_id.isnot(None),
                )
                .all()
            )

    async def create_performance_evaluation(
        self, evaluation: PerformanceEvaluationCreation
    ):
        new_evaluation = evaluation.model_dump()
        new_evaluation["scheduled"] = datetime.now()
        db_evaluation = models.PerformanceEvaluation(**new_evaluation)
        with database.create_session() as db:
            db.add(db_evaluation)
            db.commit()
            db.refresh(db_evaluation)
        return db_evaluation

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

    async def get_open_position_candidates(self, position_id):
        with database.create_session() as db:
            candidates = (
                db.query(models.PositionCandidate)
                .filter_by(open_position_id=position_id)
                .all()
            )

            return candidates

    async def update_open_position(self, position_id, candidate_id):
        with database.create_session() as db:
            open_position = (
                db.query(models.OpenPosition).filter_by(id=position_id).first()
            )
            open_position.is_open = False
            open_position.candidate_id = candidate_id
            db.commit()
            db.refresh(open_position)
            return open_position

    async def get_project_positions(self, project_id):
        with database.create_session() as db:
            positions = (
                db.query(models.OpenPosition).filter_by(project_id=project_id).all()
            )
            return positions

    async def close_project(self, project_id):
        with database.create_session() as db:
            project = db.query(models.Project).filter_by(id=project_id).first()
            project.is_team_complete = True
            db.commit()

    async def create_tecnical_test(
        self, position_id, new_technical_test: TechnicalTestResults
    ):
        dict_technical_test = new_technical_test.model_dump()
        dict_technical_test["scheduled"] = datetime.now()
        dict_technical_test["open_position_id"] = position_id
        technical_test = models.TechnicalTest(**dict_technical_test)
        with database.create_session() as db:
            db.add(technical_test)
            db.commit()
            db.refresh(technical_test)
        return technical_test

    async def create_candidate_in_position(self, position_id: int, candidate_id: int):
        with database.create_session() as db:
            new_position_candidate = models.PositionCandidate(
                open_position_id=position_id,
                candidate_id=candidate_id,
                general_score=None,
                technical_score=None,
                softskill_score=None,
            )
            db.add(new_position_candidate)
            db.commit()

            return new_position_candidate
