import pytest
from fastapi import HTTPException
from unittest.mock import Mock, AsyncMock

from app.position.services.position_service import PositionService


class TestPositionService:
    @pytest.mark.asyncio
    async def test_position_service(self):
        mocked_repository = Mock()
        mocked_repository.get_open_positions_with_details = AsyncMock()

        mock_item = (
            Mock(
                id=1,
                position_name="Test position A",
                candidate_id=1,
                project_id=1,
                is_open=False,
            ),
            Mock(
                customer_id=1,
                name="Project name",
                is_team_complete=False,
                id=1,
                description="A description",
            ),
            [1, 2],
            [3, 4],
        )

        mocked_repository.get_open_positions_with_details.return_value = [mock_item]

        service = PositionService(mocked_repository)

        result = await service.get_positions()

        assert mocked_repository.get_open_positions_with_details.call_count == 1
        assert result[0]["open_position"].id == 1
        assert result[0]["open_position"].position_name == "Test position A"
        assert result[0]["project"].id == 1
        assert not result[0]["project"].is_team_complete
        assert result[0]["soft_skill_ids"][0] == 1
        assert result[0]["technology_ids"][0] == 3

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

    @pytest.mark.asyncio
    async def test_update_position_chosen_candidate(self):
        mocked_repository = Mock()
        mocked_repository.get_open_position_candidates = AsyncMock()
        mocked_repository.update_open_position = AsyncMock()
        mocked_repository.get_project_positions = AsyncMock()
        mocked_repository.close_project = AsyncMock()

        position_id = 2
        candidate_id = 3
        project_id = 1

        position_data = Mock(candidate_id=candidate_id)

        base_candidates = [
            Mock(candidate_id=3, technical_score=0, softskill_score=0, general_score=0),
        ]
        mocked_repository.get_open_position_candidates.return_value = base_candidates

        base_position = Mock(
            id=position_id,
            project_id=project_id,
            is_open=False,
            candidate_id=candidate_id,
        )
        mocked_repository.update_open_position.return_value = base_position

        mocked_repository.get_project_positions.return_value = [base_position]

        service = PositionService(mocked_repository)

        func_response = await service.update_position_chosen_candidate(
            position_id, position_data
        )

        assert func_response.id == position_id
        assert func_response.project_id == project_id
        assert not func_response.is_open
        assert func_response.candidate_id == candidate_id

    @pytest.mark.asyncio
    async def test_update_position_candidate_was_not_preselected(self):
        mocked_repository = Mock()
        mocked_repository.get_open_position_candidates = AsyncMock()

        position_id = 2
        candidate_id = 3

        position_data = Mock(candidate_id=candidate_id)

        base_candidates = []
        mocked_repository.get_open_position_candidates.return_value = base_candidates

        service = PositionService(mocked_repository)

        with pytest.raises(HTTPException):
            await service.update_position_chosen_candidate(position_id, position_data)

    @pytest.mark.asyncio
    async def test_update_position_chosen_candidate_project_still_open(self):
        mocked_repository = Mock()
        mocked_repository.get_open_position_candidates = AsyncMock()
        mocked_repository.update_open_position = AsyncMock()
        mocked_repository.get_project_positions = AsyncMock()
        mocked_repository.close_project = AsyncMock()

        position_id = 3
        candidate_id = 4
        project_id = 2

        position_data = Mock(candidate_id=candidate_id)

        base_candidates = [
            Mock(
                candidate_id=candidate_id,
                technical_score=0,
                softskill_score=0,
                general_score=1,
            ),
        ]
        mocked_repository.get_open_position_candidates.return_value = base_candidates

        base_position = Mock(
            id=position_id,
            project_id=project_id,
            is_open=False,
            candidate_id=candidate_id,
        )
        mocked_repository.update_open_position.return_value = base_position

        base_position_2 = Mock(
            id=position_id + 1, project_id=project_id, is_open=True, candidate_id=None
        )
        mocked_repository.get_project_positions.return_value = [
            base_position,
            base_position_2,
        ]

        service = PositionService(mocked_repository)

        await service.update_position_chosen_candidate(position_id, position_data)

        assert mocked_repository.update_position_chosen_candidate.call_count == 0

    @pytest.mark.asyncio
    async def test_get_closed_positions_by_project_id(self):
        mocked_repository = Mock()
        mocked_repository.get_closed_positions_by_project_id = AsyncMock()

        service = PositionService(mocked_repository)

        await service.get_closed_positions_by_project_id(1)
        assert mocked_repository.get_closed_positions_by_project_id.call_count == 1

    @pytest.mark.asyncio
    async def test_create_position_evaluation(self):
        mocked_repository = Mock()
        mocked_repository.create_performance_evaluation = AsyncMock()

        service = PositionService(mocked_repository)

        await service.create_position_evaluation({})

        assert mocked_repository.create_performance_evaluation.call_count == 1

    @pytest.mark.asyncio
    async def test_save_technical_test_result(self):
        mocked_repository = Mock()
        mocked_repository.create_tecnical_test = AsyncMock()

        position_id = 3
        candidate_id = 4
        score = 55
        observations = "Ninguna"
        test_schedule = "2099-01-01T09:00:00"

        base_tech_test = Mock(
            scheduled=test_schedule,
            candidate_id=candidate_id,
            open_position_id=position_id,
            name="Prueba técnica A",
            score=score,
            observations=observations,
        )

        mocked_repository.create_tecnical_test.return_value = base_tech_test

        service = PositionService(mocked_repository)

        func_response = await service.save_technical_test_result(
            position_id,
            {
                "candidate_id": candidate_id,
                "name": "Prueba técnica A",
                "score": 55,
                "observations": observations,
            },
        )

        assert func_response.scheduled.isoformat() == test_schedule
        assert func_response.open_position_id == position_id
        assert func_response.candidate_id == candidate_id
        assert func_response.score == score
        assert func_response.observations == observations
