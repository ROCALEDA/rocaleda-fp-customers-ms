from unittest.mock import patch

from app.health.controllers import health_controller


class TestHealthController:
    @patch.object(health_controller, "HealthService")
    def test_get_health(self, MockHealthService):
        mock_service_instance = MockHealthService.return_value
        mock_service_instance.get_health.return_value = {"status": "Ok"}

        get_health = health_controller.initialize(mock_service_instance)

        response = get_health()

        assert response == {"status": "Ok"}
        assert mock_service_instance.get_health.call_count == 1
