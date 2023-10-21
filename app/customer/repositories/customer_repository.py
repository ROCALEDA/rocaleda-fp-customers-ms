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
            return project.id

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

