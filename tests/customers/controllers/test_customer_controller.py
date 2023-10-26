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
