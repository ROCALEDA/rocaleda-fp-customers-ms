from datetime import datetime
from typing import Annotated, List, Optional
from pydantic import BaseModel, Field


# Request Push de Pub/Sub
class PubSubMessage(BaseModel):
    message: dict


# Elemento base empresa
class CustomerBase(BaseModel):
    user_id: int
    name: str


# Elemento base posición
class PositionCreationBase(BaseModel):
    name: str
    soft_skills: List[str]
    tech_skills: List[str]


# Elemento base creación de posición
class ProfileCreation(PositionCreationBase):
    amount: Annotated[int, Field(strict=True, gt=0, le=50)]


# Elementos funcionario
class EmployeeBase(BaseModel):
    full_name: str
    profile_name: str


# Request creación de proyecto
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


# Elemento base posición en respuesta de proyecto
class PositionDetailResponse(BaseModel):
    id: int
    is_open: bool
    name: str


# Respuesta proyectos detallados de cliente empresa
class ProjectDetailResponse(BaseModel):
    id: int
    name: str
    is_team_complete: bool
    total_positions: int
    positions: List[PositionDetailResponse]


# Respuesta candidato a posición
class CandidateResponse(BaseModel):
    candidate_id: int
    technical_score: Optional[int]
    softskill_score: Optional[int]
    general_score: Optional[int]


# Request actualización detalle de posición
class PositionUpdate(BaseModel):
    candidate_id: int


# Respuesta actualización detalles de posición
class PositionUpdateResponse(BaseModel):
    id: int
    project_id: int
    is_open: bool
    candidate_id: int


# Request guardado datos prueba de desempeño
class PerformanceEvaluationCreation(BaseModel):
    project_id: int
    name: str
    candidate_id: int
    score: int
    observations: str


# Respuesta consulta de detalle empresas cliente
class CustomersResponse(BaseModel):
    data: List[CustomerBase]
    total_pages: int


# Request guardar resultado prueba técnica para admisión
class TechnicalTestResults(BaseModel):
    candidate_id: int
    name: str
    score: int
    observations: str


# Respuesta guardado resultado prueba técnica para admisión
class TechnicalTestResponse(BaseModel):
    scheduled: datetime
    open_position_id: int
    candidate_id: int
    score: int
    observations: str
