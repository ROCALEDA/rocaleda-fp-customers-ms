import pytest
from unittest.mock import Mock, AsyncMock

from app.database.schemas import CustomerBase
from app.customer.services.customer_service import CustomerService


class TestCustomerService:
    @pytest.mark.asyncio
    async def test_create_customer(self):
        mocked_repository = Mock()

        mocked_repository.create_customer = AsyncMock()

        service = CustomerService(mocked_repository)

        new_customer = CustomerBase(user_id=1, name="ACME")

        await service.create_customer(new_customer)

        mocked_repository.create_customer.assert_called_once_with(
            {
                "user_id": new_customer.user_id,
                "name": new_customer.name,
            }
        )
