import pytest
from unittest.mock import Mock, AsyncMock

from app.database.schemas import CustomerBase, ProjectCreation, ProjectCreationResponse
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
        customer_id = 1

        mocked_repository = Mock()

        mocked_repository.create_project = AsyncMock()
        mocked_repository.create_project.return_value = ProjectCreationResponse(
            id=1,
            name="Proyecto Test",
            description="Proyecto Test Description",
        )

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
        project = ProjectCreation(**project_data)

        await customer_service.create_project(customer_id, project)

        mocked_repository.create_project.assert_called_once_with(
            {
                "customer_id": customer_id,
                "name": "Test Project",
                "description": "Test Project description",
            }
        )
        assert mocked_repository.create_employee.call_count == 2
        assert mocked_repository.create_open_position.call_count == 2

    @pytest.mark.asyncio
    async def test_get_customer_projects(self):
        mocked_repository = Mock()
        mocked_repository.get_projects = AsyncMock()

        open_positions_a = Mock(
            id=1, is_open=False, position_name="Test position A", candidate_id=1
        )
        open_positions_b = Mock(
            id=2, is_open=False, position_name="Test position B", candidate_id=2
        )

        project_1 = Mock(
            id=1, is_team_complete=False, total_positions=2, open_positions=[]
        )
        project_2 = Mock(
            id=2,
            is_team_complete=True,
            total_positions=1,
            open_positions=[open_positions_a, open_positions_b],
        )
        project_2.name = "Test Project 2"

        base_projects = [project_1, project_2]

        mocked_repository.get_projects.return_value = base_projects

        service = CustomerService(mocked_repository)

        customer_id = 2

        func_response = await service.get_customer_projects(customer_id)
        print(func_response)

        assert len(func_response) == 2
        assert func_response[1]["name"] == "Test Project 2"
        assert func_response[1]["is_team_complete"]
        assert func_response[1]["total_positions"] == 2
        assert len(func_response[1]["positions"]) == 2
        assert func_response[1]["positions"][1]["id"] == 2
        assert not func_response[1]["positions"][1]["is_open"]
        assert func_response[1]["positions"][1]["name"] == "Test position B"
