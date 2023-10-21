import pytest
from unittest.mock import Mock, AsyncMock

from app.database.schemas import CustomerBase, ProjectCreate
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

    @pytest.mark.asyncio
    async def test_create_project(self):
        mocked_repository = Mock()

        mocked_repository.create_project = AsyncMock()
        mocked_repository.create_project.return_value = 1

        mocked_repository.create_employee = AsyncMock()

        mocked_soft_skill = Mock(id=1, name="Responsibility")
        mocked_repository.get_soft_skill_by_name = AsyncMock()
        mocked_repository.get_soft_skill_by_name.return_value = mocked_soft_skill

        mocked_tech_skill = Mock(id=1, name="NodeJS")
        mocked_repository.get_tech_skill_by_name = AsyncMock()
        mocked_repository.get_tech_skill_by_name.return_value = mocked_tech_skill

        mocked_repository.create_open_position = AsyncMock()

        customer_service = CustomerService(mocked_repository)

        project_data = {
            "customer_id": 1,
            "name": "Test Project",
            "description": "Test Project description",
            "profiles": [
                {
                    "name": "Profile 1",
                    "tech_skills": ["Frontend"],
                    "soft_skills": ["Leadership"],
                    "amount": 1,
                },
                {
                    "name": "Profile 2",
                    "tech_skills": ["Backend"],
                    "soft_skills": ["Responsibility"],
                    "amount": 1,
                },
            ],
            "employees": [
                {"full_name": "Employee 1", "profile_name": "Employee profile 1"},
                {"full_name": "Employee 2", "profile_name": "Employee profile 2"},
            ],
            "state": {"role_id": 1, "email": "test@examplemail.com", "user_id": 1},
        }
        project = ProjectCreate(**project_data)

        await customer_service.create_project(project)

        mocked_repository.create_project.assert_called_once_with(
            {
                "customer_id": 1,
                "name": "Test Project",
                "description": "Test Project description",
            }
        )
        assert mocked_repository.create_employee.call_count == 2
        assert mocked_repository.create_open_position.call_count == 2
