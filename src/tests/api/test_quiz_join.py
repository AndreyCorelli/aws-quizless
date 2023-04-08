import pytest

from src.domain.quiz_requests import QuizStartRequest, QuizJoinRequest
from src.tests.api.api_test_client import responses_client, HEADER_JSON_CONTENT_TYPE, start_quiz


@pytest.mark.asyncio
async def test_quiz_join():
    quiz_code, _user_token = await start_quiz()

    response = await responses_client.post(
        "/api/quiz-join", json=QuizJoinRequest(
            quiz_code=quiz_code,
            user_name="C"
        ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)
    assert response.status_code == 200
    res_json = response.json()
    assert "state" in res_json
    assert "user" in res_json
