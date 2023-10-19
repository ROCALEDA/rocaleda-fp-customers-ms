import base64
import json
import pytest
from fastapi import HTTPException
from unittest.mock import Mock, AsyncMock

from app.customer.controllers import customer_controller


class TestCustomerController:
    @pytest.mark.asyncio
    async def test_create_customer_from_push(self):
        mock_service = Mock()
        mock_service.create_customer = AsyncMock()

        data_to_encode = {"user_id": 1, "name": "ACME"}
        json_str = json.dumps(data_to_encode)
        encoded_data = base64.b64encode(json_str.encode("utf-8"))

        data_mock = Mock(message={"data": encoded_data})

        create_customer_func = customer_controller.initialize(mock_service)[
            "create_customer_from_push"
        ]

        response = await create_customer_func(data_mock)

        assert "success" in response

        
