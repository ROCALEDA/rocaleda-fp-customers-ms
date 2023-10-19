from fastapi import APIRouter

from app.health.services.health_service import HealthService

router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)


def initialize(health_service: HealthService):
    @router.get("/")
    def get_health():
        return health_service.get_health()

    return get_health
