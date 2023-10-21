from typing import Annotated, List

from pydantic import BaseModel, Field


# Request Push de Pub/Sub
class PubSubMessage(BaseModel):
    message: dict


# Request nueva empresa
class CustomerBase(BaseModel):
    user_id: int
    name: str


# Elementos basicos nuevo proyecto
class ProjectBase(BaseModel):
    name: str
    description: str


# Elementos perfil
class ProfileBase(BaseModel):
    name: str
    soft_skills: List[str]
    tech_skills: List[str]
    amount: Annotated[int, Field(strict=True, gt=0, le=50)]


# Elementos funcionario
class EmployeeBase(BaseModel):
    # project_id : int
    full_name: str
    profile_name: str


# Request nuevo proyecto
class ProjectCreate(ProjectBase):
    profiles: List[ProfileBase]
    employees: List[EmployeeBase]


# Response creación proyecto
class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
