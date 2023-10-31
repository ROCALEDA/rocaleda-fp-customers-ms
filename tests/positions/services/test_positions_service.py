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
