from typing import Annotated, List, Optional
from pydantic import BaseModel, Field


# Request Push de Pub/Sub
class PubSubMessage(BaseModel):
    message: dict


# Request nueva empresa
class CustomerBase(BaseModel):
    user_id: int
    name: str


class PositionBase(BaseModel):
    name: str
    soft_skills: List[str]
    tech_skills: List[str]


# Elementos perfil
class ProfileCreation(PositionBase):
    amount: Annotated[int, Field(strict=True, gt=0, le=50)]


# Elementos funcionario
class EmployeeBase(BaseModel):
    full_name: str
    profile_name: str


# Request nuevo proyecto
class ProjectCreation(BaseModel):
    name: str
    description: str
    profiles: List[ProfileCreation]
    employees: List[EmployeeBase]


# Response creación proyecto
class ProjectCreationResponse(BaseModel):
    id: int
    name: str
    description: str


class PositionDetailResponse(BaseModel):
    id: int
    is_open: bool
    name: str


class ProjectDetailResponse(BaseModel):
    id: int
    name: str
    is_team_complete: bool
    total_positions: int
    positions: List[PositionDetailResponse]


class CandidateResponse(BaseModel):
    candidate_id: int
    technical_score: Optional[int]
    softskill_score: Optional[int]
    general_score: Optional[int]
