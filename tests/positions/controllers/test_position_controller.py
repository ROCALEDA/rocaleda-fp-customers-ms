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
