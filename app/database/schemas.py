from typing import Annotated, List

from pydantic import BaseModel, Field

# Elementos identidad cliente de API
class StateBase(BaseModel):
    role_id : str
    email : str
    user_id : str

# Request Push de Pub/Sub
class PubSubMessage(BaseModel):
    message: dict


# Request nueva empresa
class CustomerBase(BaseModel):
    user_id: int
    name: str


# Elementos basicos nuevo proyecto
class ProjectBase(BaseModel):
    state: StateBase
    name: str
    description: str


# Elementos perfil
class ProfileBase(BaseModel):
    name: str
    tech_skills: List[str]
    soft_skills: List[str]
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
