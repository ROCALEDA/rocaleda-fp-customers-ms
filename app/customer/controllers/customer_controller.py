import base64
import json
from fastapi import APIRouter, Body, HTTPException
from typing import List, TYPE_CHECKING

from app.database.schemas import (
    PubSubMessage,
    CustomerBase,
    ProjectCreation,
    ProjectCreationResponse,
    ProjectDetailResponse,
)

if TYPE_CHECKING:
    from app.customer.services.customer_service import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["customer"],
    responses={404: {"description": "Not found"}},
)


def initialize(customer_service: "CustomerService"):
    @router.post("/push")
    async def create_customer_from_push(data: PubSubMessage = Body(...)):
        message = data.message
        if not message:
            raise HTTPException(status_code=400, detail="Invalid message format")
        decoded_data = base64.b64decode(message["data"]).decode("utf-8")
        data_dict = json.loads(decoded_data)
        print("Received message from pubsub: ", data_dict)

        customer = CustomerBase(**data_dict)
        await customer_service.create_customer(customer)

        return {"success": True}

    @router.post("/{customer_id}/projects")
    async def create_project(
        customer_id: int, project: ProjectCreation
    ) -> ProjectCreationResponse:
        return await customer_service.create_project(customer_id, project)

    @router.get("/{customer_id}/projects")
    async def get_customer_projects(customer_id: int) -> List[ProjectDetailResponse]:
        return await customer_service.get_customer_projects(customer_id)

    return {
        "create_customer_from_push": create_customer_from_push,
        "create_project": create_project,
        "get_customer_projects": get_customer_projects,
    }
