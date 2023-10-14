from pydantic import BaseModel

class CustomerBase(BaseModel):
    id: int
    userId: int
    name: str
