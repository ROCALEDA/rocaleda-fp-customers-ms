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
