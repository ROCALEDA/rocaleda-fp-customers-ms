from app.health.services.health_service import HealthService


service = HealthService()


class TestHealthService:
    def test_get_health(self):
        response = service.get_health()

        assert response == {"status": "Ok"}
