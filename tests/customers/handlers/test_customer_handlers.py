import json
import pytest
from unittest.mock import Mock, AsyncMock
from app.customer.handlers.customer_handlers import create_customer_handler

class TestCustomerHandler:
    @pytest.mark.asyncio
    async def test_create_customer_handler(self):
        mocked_service = Mock()
        mocked_service.create_customer = AsyncMock()

        handler = await create_customer_handler(mocked_service)

        mocked_customer = {
            "user_id": 1,
            "name": "ACME"
        }

        message_mock =json.dumps(mocked_customer).encode("utf-8")

        await handler(message_mock)

        assert mocked_service.create_customer.call_count == 1