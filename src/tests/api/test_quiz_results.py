from typing import List, Any, Dict

from freezegun import freeze_time
import pytest

from domain.quiz_requests import QuizJoinRequest, ScheduleQuizRequest, QuizStatusRequest, \
    StoreAnswerRequest
from tests.api.api_test_client import responses_client, HEADER_JSON_CONTENT_TYPE, start_quiz


@pytest.mark.asyncio
@freeze_time("2020-11-12 10:00:00.000")
async def test_quiz_results():
    quiz_code, first_user_token = await start_quiz()
    second_user_token = await _let_second_player_join(quiz_code)
    await _schedule_quiz(first_user_token, quiz_code)

    with freeze_time("2020-11-12 10:00:02.200"):
        await _give_answer(first_user_token, quiz_code, 0, [2])
    with freeze_time("2020-11-12 10:00:03.200"):
        await _give_answer(second_user_token, quiz_code, 0, [2])
    with freeze_time("2020-11-12 10:00:17.200"):
        await _give_answer(second_user_token, quiz_code, 1, [0, 1])
    with freeze_time("2020-11-12 10:00:30.200"):
        res = await _check_state(second_user_token, quiz_code)
        assert res["state"]["status"] == "FINISHED"

        res_json = await responses_client.get(
            f"/api/quiz-results/{quiz_code}")
        res = res_json.json()
        assert res["quiz_data"]
        assert res["quiz_results"]
        players_result = res["quiz_results"]["players"]
        assert len(players_result) == 2


async def _check_state(
        user_token: str, quiz_code: int) -> Dict[str, Any]:
    res_json = await responses_client.post(
        "/api/quiz-check-status", json=QuizStatusRequest(
            quiz_code=quiz_code,
            user_token=user_token
        ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)
    return res_json.json()


async def _give_answer(
        user_token: str, quiz_code: int,
        question_index: int, answer: List[int]) -> None:
    await responses_client.post(
        "/api/quiz-answer", json=StoreAnswerRequest(
            quiz_code=quiz_code,
            user_token=user_token,
            question_index=question_index,
            answer=answer
        ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)


async def _schedule_quiz(first_user_token, quiz_code):
    await responses_client.post(
        "/api/quiz-schedule", json=ScheduleQuizRequest(
            quiz_code=quiz_code,
            user_token=first_user_token,
            delay_seconds=2
        ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)


async def _let_second_player_join(quiz_code: int) -> str:
    response = await responses_client.post(
        "/api/quiz-join", json=QuizJoinRequest(
            quiz_code=quiz_code,
            user_name="Second"
        ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)
    assert response.status_code == 200
    res_json = response.json()
    assert "state" in res_json
    return res_json["user"]["user_token"]
