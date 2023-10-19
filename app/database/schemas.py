from pydantic import BaseModel


class CustomerBase(BaseModel):
    user_id: int
    name: str


class PubSubMessage(BaseModel):
    message: dict