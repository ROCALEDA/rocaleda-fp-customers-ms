import os

os.environ["DB_URL"] = "postgresql://postgres:mock@10.10.10.10:5432/customers"
import pytest
from app.customer.repositories.customer_repository import CustomerRepository
from app.database import models


@pytest.fixture
def mock_session(mocker):
    session_class = mocker.patch("app.database.database.SessionLocal")
    return session_class.return_value


@pytest.fixture
async def customer_repository(mock_session):
    return CustomerRepository()


@pytest.mark.asyncio
async def test_create_customer(mock_session, customer_repository):
    new_customer = {"user_id": 1, "name": "Prueba empresa"}
    repository = await customer_repository
    await repository.create_customer(new_customer)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
