import pytest
from unittest.mock import Mock, AsyncMock

from app.position.controllers import position_controller


class TestPositionController:
    @pytest.mark.asyncio
    async def test_position_controller(self):
        mocked_service = Mock()
        mocked_service.get_positions = AsyncMock()

        get_positions_func = position_controller.initialize(mocked_service)[
            "get_positions"
        ]

        await get_positions_func()

        assert mocked_service.get_positions.call_count == 1

    @pytest.mark.asyncio
    async def test_get_position_candidates(self):
        mocked_service = Mock()
        mocked_service.get_position_candidates = AsyncMock()

        candidates_data = [
            {
                "candidate_id": 1,
                "technical_score": 1,
                "softskill_score": 2,
                "general_score": 3,
            },
            {
                "candidate_id": 2,
                "technical_score": None,
                "softskill_score": None,
                "general_score": None,
            },
        ]
        mocked_service.get_position_candidates.return_value = candidates_data

        position_id = 1

        get_position_candidates_func = position_controller.initialize(mocked_service)[
            "get_position_candidates"
        ]

        func_response = await get_position_candidates_func(position_id)

        mocked_service.get_position_candidates.assert_called_once_with(position_id)
        assert func_response == candidates_data

    @pytest.mark.asyncio
    async def test_update_position_chosen_candidate(self):
        mocked_service = Mock()
        mocked_service.update_position_chosen_candidate = AsyncMock()

        position_id = 2

        request_body = {"candidate_id": 3}

        updated_position = {
            "id": position_id,
            "project_id": 1,
            "is_open": False,
            "candidate_id": 3,
        }
        mocked_service.update_position_chosen_candidate.return_value = updated_position

        update_position_chosen_candidate_func = position_controller.initialize(
            mocked_service
        )["update_position_chosen_candidate"]

        await update_position_chosen_candidate_func(position_id, request_body)

        assert mocked_service.update_position_chosen_candidate.call_count == 1

    @pytest.mark.asyncio
    async def test_get_closed_positions_by_project_id(self):
        mocked_service = Mock()
        mocked_service.get_closed_positions_by_project_id = AsyncMock()
        mocked_service.get_closed_positions_by_project_id.return_value = []

        get_closed_positions_by_project_id_func = position_controller.initialize(
            mocked_service
        )["get_closed_positions_by_project_id"]

        await get_closed_positions_by_project_id_func(1)
        assert mocked_service.get_closed_positions_by_project_id.call_count == 1

    @pytest.mark.asyncio
    async def test_create_position_evaluation(self):
        mocked_service = Mock()
        mocked_service.create_position_evaluation = AsyncMock()
        mocked_service.create_position_evaluation.return_value = {}

        create_position_evaluation_func = position_controller.initialize(
            mocked_service
        )["create_position_evaluation"]

        await create_position_evaluation_func({})
        assert mocked_service.create_position_evaluation.call_count == 1

    @pytest.mark.asyncio
    async def test_save_technical_test_result(self):
        mocked_service = Mock()
        mocked_service.save_technical_test_result = AsyncMock()

        position_id = 3
        candidate_id = 4
        score = 55
        observations = "Ninguna"

        request_body = {
            "candidate_id": candidate_id,
            "name": "Prueba técnica A",
            "score": 55,
            "observations": observations,
        }

        updated_tech_test = {
            "scheduled": "2099-01-01T09:00:00.000Z",
            "open_position_id": position_id,
            "candidate_id": candidate_id,
            "score": score,
            "observations": observations,
        }
        mocked_service.save_technical_test_result.return_value = updated_tech_test

        save_technical_test_result_func = position_controller.initialize(
            mocked_service
        )["save_technical_test_result"]

        await save_technical_test_result_func(position_id, request_body)

        assert mocked_service.save_technical_test_result.call_count == 1
