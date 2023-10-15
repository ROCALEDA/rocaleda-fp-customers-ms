from typing import TYPE_CHECKING

from app.database.schemas import CustomerBase

if TYPE_CHECKING:
    from app.customer.repositories.customer_repository import CustomerRepository

class CustomerService:

    def __init__(self, customer_repository: "CustomerRepository"):
        self.customer_repository = customer_repository
    
    async def create_customer(self, new_customer: CustomerBase) -> None:

        new_customer_dict = {
            "user_id": new_customer.user_id,
            "name": new_customer.name
        }

        await self.customer_repository.create_customer(new_customer_dict)