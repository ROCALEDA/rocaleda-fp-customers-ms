import pytest
from unittest.mock import Mock, AsyncMock

from app.position.services.position_service import PositionService


class TestPositionService:
    @pytest.mark.asyncio
    async def test_position_service(self):
        mocked_repository = Mock()
        mocked_repository.get_open_positions_with_details = AsyncMock()

        service = PositionService(mocked_repository)

        await service.get_positions()

        assert mocked_repository.get_open_positions_with_details.call_count == 1

    @pytest.mark.asyncio
    async def test_get_position_candidates(self):
        mocked_repository = Mock()
        mocked_repository.get_open_position_candidates = AsyncMock()

        base_candidates = [
            Mock(candidate_id=1, technical_score=1, softskill_score=2, general_score=3),
            Mock(
                candidate_id=2,
                technical_score=None,
                softskill_score=None,
                general_score=None,
            ),
        ]
        mocked_repository.get_open_position_candidates.return_value = base_candidates

        service = PositionService(mocked_repository)

        position_id = 1

        func_response = await service.get_position_candidates(position_id)

        assert len(func_response) == 2
        assert func_response[0]["candidate_id"] == 1
        assert func_response[0]["technical_score"] == 1
        assert func_response[0]["softskill_score"] == 2
        assert func_response[0]["general_score"] == 3
