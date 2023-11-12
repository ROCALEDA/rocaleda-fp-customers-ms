import base64
import json
import pytest
from fastapi import HTTPException
from unittest.mock import Mock, AsyncMock

from app.customer.controllers import customer_controller
from app.database.schemas import ProjectCreation


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

    @pytest.mark.asyncio
    async def test_create_customer_from_push_to_raise_exc(self):
        mock_service = Mock()
        mock_service.create_customer = AsyncMock()

        data_mock = Mock(message=None)

        create_customer_func = customer_controller.initialize(mock_service)[
            "create_customer_from_push"
        ]

        with pytest.raises(HTTPException):
            await create_customer_func(data_mock)

    @pytest.mark.asyncio
    async def test_create_project(self):
        mocked_service = Mock()
        mocked_service.create_project = AsyncMock()

        customer_id = 1

        create_project_func = customer_controller.initialize(mocked_service)[
            "create_project"
        ]

        project_data = {
            "name": "Test Project",
            "description": "Test Project description",
            "profiles": [
                {
                    "name": "Profile 1",
                    "tech_skills": ["Frontend"],
                    "soft_skills": ["Leadership"],
                    "amount": 1,
                }
            ],
            "employees": [
                {"full_name": "Employee 1", "profile_name": "Employee profile 1"}
            ],
            "state": {"role_id": 1, "email": "test@examplemail.com", "user_id": 1},
        }

        project = ProjectCreation(**project_data)

        await create_project_func(customer_id, project)
        assert mocked_service.create_project.call_count == 1
        mocked_service.create_project.assert_called_once_with(customer_id, project)

    @pytest.mark.asyncio
    async def test_get_customer_projects(self):
        mocked_service = Mock()
        mocked_service.get_customer_projects = AsyncMock()

        projects_data = [
            {
                "id": 1,
                "name": "Test Project 1",
                "is_team_complete": False,
                "total_positions": 2,
                "open_positions": [
                    {
                        "id": 1,
                        "is_open": True,
                        "name": "Test Position A",
                    },
                    {
                        "id": 2,
                        "is_open": True,
                        "name": "Test Position B",
                    },
                ],
            },
            {
                "id": 2,
                "name": "Test Project 2",
                "is_team_complete": True,
                "total_positions": 1,
                "open_positions": [
                    {
                        "id": 3,
                        "is_open": True,
                        "name": "Test Position C",
                    }
                ],
            },
        ]
        mocked_service.get_customer_projects.return_value = projects_data

        customer_id = 2

        get_customer_projects_func = customer_controller.initialize(mocked_service)[
            "get_customer_projects"
        ]

        func_response = await get_customer_projects_func(customer_id)

        mocked_service.get_customer_projects.assert_called_once_with(customer_id)
        assert func_response == projects_data

    @pytest.mark.asyncio
    async def test_get_customers(self):
        mocked_service = Mock()
        mocked_service.get_customers = AsyncMock()

        customers_data = {
            "data": [
                {
                    "user_id": 1,
                    "name": "Customer A",
                },
                {
                    "user_id": 2,
                    "name": "Customer B",
                },
            ],
            "total_pages": 1,
        }
        mocked_service.get_customers.return_value = customers_data

        get_customers_func = customer_controller.initialize(mocked_service)[
            "get_customers"
        ]

        ids = "1,2"
        page = 1
        limit = 100

        func_response = await get_customers_func(ids, page, limit)

        mocked_service.get_customers.assert_called_once_with(
            id_list=['1','2'], page=page, limit=limit
        )
        assert func_response == customers_data
