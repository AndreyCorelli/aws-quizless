import pytest

from src.domain.quiz_requests import QuizStartRequest
from src.tests.api.api_test_client import responses_client, HEADER_JSON_CONTENT_TYPE


@pytest.mark.asyncio
async def test_quiz_start():
    response = await responses_client.post(
        "/api/quiz-start", json=QuizStartRequest(
            topic_id="73b445cc-34c6-482d-bf44-0db2f3a06e05",
            user_name="B",
            question_seconds=13
        ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["state"]
    assert res_json["state"]["name"] == "Animal quiz"
