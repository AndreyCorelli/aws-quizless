from freezegun import freeze_time
import pytest

from domain.quiz_requests import ScheduleQuizRequest, QuizStatusRequest
from tests.api.api_test_client import responses_client, HEADER_JSON_CONTENT_TYPE, start_quiz


@pytest.mark.asyncio
@freeze_time("2020-11-12 10:00:00.000")
async def test_check_quiz_state():
    quiz_code, user_token = await start_quiz()

    await responses_client.post(
        "/api/quiz-schedule", json=ScheduleQuizRequest(
            quiz_code=quiz_code,
            user_token=user_token,
            delay_seconds=2
        ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)

    with freeze_time("2020-11-12 10:00:02.200"):
        response = await responses_client.post(
            "/api/quiz-check-status", json=QuizStatusRequest(
                quiz_code=quiz_code,
                user_token=user_token
            ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)
        res_json = response.json()
        assert "state" in res_json
        assert res_json["state"]["status"] == "STARTED"
        assert res_json["state"]["cur_question_index"] == [0, 2]
