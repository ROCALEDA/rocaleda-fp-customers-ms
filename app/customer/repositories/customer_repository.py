from app.database import models, database


class CustomerRepository:
    async def create_customer(self, new_customer: dict):
        customer = models.Customer(**new_customer)
        with database.create_session() as db:
            db.add(customer)
            db.commit()

    async def create_project(self, new_project: dict):
        project = models.Project(**new_project)
        with database.create_session() as db:
            db.add(project)
            db.commit()
            db.refresh(project)
        return project

    async def create_employee(self, new_employee: dict):
        employee = models.Employee(**new_employee)
        with database.create_session() as db:
            db.add(employee)
            db.commit()

    async def create_open_position(self, new_open_position: dict):
        open_position = models.OpenPosition(**new_open_position)
        with database.create_session() as db:
            db.add(open_position)
            db.commit()

    async def get_soft_skill_by_name(self, name: str) -> models.SoftSkill:
        with database.create_session() as db:
            return db.query(models.SoftSkill).filter_by(name=name).first()

    async def get_tech_skill_by_name(self, name: str) -> models.Technology:
        with database.create_session() as db:
            return db.query(models.Technology).filter_by(name=name).first()

    async def get_projects(self, customer_id: int):
        with database.create_session() as db:
            projects = db.query(models.Project).filter_by(customer_id=customer_id).all()
            for project in projects:
                project.open_positions
            return projects

    async def get_customers_filtered(self, ids: list, page: int, per_page: int):
        with database.create_session() as db:
            total_pages = 1
            if ids is not None and len(ids) > 0:
                query = db.query(models.Customer).filter(
                    models.Customer.user_id.in_(ids)
                )
            else:
                query = db.query(models.Customer)
            if per_page is not None:
                total_count = query.count()
                total_pages = (total_count + per_page - 1) // per_page
                offset = (page - 1) * per_page
                query = query.offset(offset).limit(per_page)
            return {"data": query.all(), "total_pages": total_pages}

    async def get_performance_evaluations_by_project_ids(self, ids: list[int]):
        with database.create_session() as db:
            evaluations = (
                db.query(models.PerformanceEvaluation)
                .filter(models.PerformanceEvaluation.project_id.in_(ids))
                .all()
            )
            return evaluations

    async def get_performance_evaluations_by_candidate_id(self, id: int):
        with database.create_session() as db:
            evaluations = (
                db.query(models.PerformanceEvaluation).filter_by(candidate_id=id).all()
            )
            return evaluations
          
    async def get_project_positions(self, id: int):
        with database.create_session() as db:
            return db.query(models.OpenPosition).filter_by(project_id=id).all()

    async def get_technical_tests_by_position_ids(self, ids: list[int]):
        with database.create_session() as db:
            tests = (
                db.query(models.TechnicalTest)
                .filter(models.TechnicalTest.open_position_id.in_(ids))
                .all()
            )
            return tests

    async def get_technical_tests_by_candidate_id(self, id: int):
        with database.create_session() as db:
            return db.query(models.TechnicalTest).filter_by(candidate_id=id).all()
