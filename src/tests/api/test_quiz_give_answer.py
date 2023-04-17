import time

from freezegun import freeze_time
import pytest

from domain.quiz_requests import QuizStartRequest, QuizJoinRequest, ScheduleQuizRequest, QuizStatusRequest, \
    StoreAnswerRequest
from tests.api.api_test_client import responses_client, HEADER_JSON_CONTENT_TYPE, start_quiz


@pytest.mark.asyncio
@freeze_time("2020-11-12 10:00:00.000")
async def test_give_answer():
    quiz_code, user_token = await start_quiz()

    await responses_client.post(
        "/api/quiz-schedule", json=ScheduleQuizRequest(
            quiz_code=quiz_code,
            user_token=user_token,
            delay_seconds=2
        ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)

    with freeze_time("2020-11-12 10:00:02.200"):
        response = await responses_client.post(
            "/api/quiz-answer", json=StoreAnswerRequest(
                quiz_code=quiz_code,
                user_token=user_token,
                question_index=0,
                answer=[2]
            ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)
        res_json = response.json()
        assert "state" in res_json
        assert res_json["state"]["status"] == "STARTED"
        assert res_json["state"]["cur_question_index"] == [0, 2]
        assert res_json["user"]["answers"][0]["answer"] == [2]
        assert res_json["user"]["answers"][0]["answer_given_seconds"] == 0

    with freeze_time("2020-11-12 10:00:04.200"):
        response = await responses_client.post(
            "/api/quiz-answer", json=StoreAnswerRequest(
                quiz_code=quiz_code,
                user_token=user_token,
                question_index=0,
                answer=[2]
            ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)
        res_json = response.json()
        assert res_json["state"]["cur_question_index"] == [0, 2]
        assert res_json["user"]["answers"][0]["answer"] == [2]
        assert res_json["user"]["answers"][0]["answer_given_seconds"] == 2

    with freeze_time("2020-11-12 10:00:15.200"):
        response = await responses_client.post(
            "/api/quiz-answer", json=StoreAnswerRequest(
                quiz_code=quiz_code,
                user_token=user_token,
                question_index=1,
                answer=[0, 1]
            ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)
        res_json = response.json()
        assert res_json["state"]["cur_question_index"] == [1, 2]
        assert res_json["user"]["answers"][1]["answer"] == [0, 1]
        assert res_json["user"]["answers"][1]["answer_given_seconds"] == 0
