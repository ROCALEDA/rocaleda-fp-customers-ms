from app.database import models, database

class CustomerRepository:
    async def create_customer(self, new_customer: dict):
        customer = models.Customer(**new_customer)
        with database.create_session() as db:
            db.add(customer)
            db.commit()
    