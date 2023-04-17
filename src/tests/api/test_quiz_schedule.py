import time

from freezegun import freeze_time
import pytest

from domain.quiz_requests import QuizStartRequest, QuizJoinRequest, ScheduleQuizRequest, QuizStatusRequest
from tests.api.api_test_client import responses_client, HEADER_JSON_CONTENT_TYPE, start_quiz


@pytest.mark.asyncio
async def test_quiz_schedule():
    quiz_code, user_token = await start_quiz()

    response = await responses_client.post(
        "/api/quiz-schedule", json=ScheduleQuizRequest(
            quiz_code=quiz_code,
            user_token=user_token,
            delay_seconds=2
        ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)
    assert response.status_code == 200
    res_json = response.json()
    assert "state" in res_json
    assert res_json["state"]["status"] == "SCHEDULED"
    assert "user" in res_json


@pytest.mark.asyncio
@freeze_time("2020-11-12 10:00:00.000")
async def test_quiz_started_automatically():
    quiz_code, user_token = await start_quiz()

    response = await responses_client.post(
        "/api/quiz-schedule", json=ScheduleQuizRequest(
            quiz_code=quiz_code,
            user_token=user_token,
            delay_seconds=2
        ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)
    res_json = response.json()
    assert "state" in res_json
    assert res_json["state"]["status"] == "SCHEDULED"

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
        assert res_json["state"]["cur_question"]["text"]
        assert not res_json["state"]["cur_question"]["correct_answers"]
        assert len(res_json["state"]["cur_question"]["answers"]) == 3

    with freeze_time("2020-11-12 10:00:015.200"):
        response = await responses_client.post(
            "/api/quiz-check-status", json=QuizStatusRequest(
                quiz_code=quiz_code,
                user_token=user_token
            ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)
        res_json = response.json()
        assert res_json["state"]["status"] == "STARTED"
        assert res_json["state"]["cur_question_index"] == [1, 2]
        assert res_json["state"]["cur_question"]["text"]
        assert not res_json["state"]["cur_question"]["correct_answers"]
        assert len(res_json["state"]["cur_question"]["answers"]) == 4
