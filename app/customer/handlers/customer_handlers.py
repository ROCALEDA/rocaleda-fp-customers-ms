import json
from typing import Any
from typing import TYPE_CHECKING
from app.database.schemas import CustomerBase

if TYPE_CHECKING:
    from app.customer.services.customer_service import CustomerService


async def create_customer_handler(service: "CustomerService"):
    async def handler(message: Any) -> None:
        parsed_message = json.loads(message.decode("utf-8"))
        print(f"Parsed message {(parsed_message)}")
        parsed_message = CustomerBase.model_validate(parsed_message)
        await service.create_customer(parsed_message)

    return handler
