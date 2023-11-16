import pytest
from app.customer.repositories.customer_repository import CustomerRepository
from app.position.repositories.position_repository import PositionRepository
from app.database.schemas import TechnicalTestResults


@pytest.fixture
def mock_session(mocker):
    session_class = mocker.patch("app.database.database.SessionLocal")
    return session_class.return_value


@pytest.fixture
async def customer_repository(mock_session):
    return CustomerRepository()


@pytest.fixture
async def position_repository(mock_session):
    return PositionRepository()


@pytest.mark.asyncio
async def test_create_customer(mock_session, customer_repository):
    new_customer = {"user_id": 1, "name": "Prueba empresa"}
    repository = await customer_repository
    await repository.create_customer(new_customer)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_tecnical_test(mock_session, position_repository):
    new_technical_test = TechnicalTestResults.model_validate(
        {
            "scheduled": "2099-01-01T00:00:00",
            "candidate_id": 1,
            "open_position_id": 1,
            "name": "Test prueba",
            "score": 100,
            "observations": "Ninguna",
        }
    )
    repository = await position_repository
    await repository.create_tecnical_test(1, new_technical_test)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
