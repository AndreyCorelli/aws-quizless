from typing import Tuple

from httpx import AsyncClient

from main import app
from domain.quiz_requests import QuizStartRequest

TEST_BASE_URL = "http://test"
HEADER_JSON_CONTENT_TYPE = {"Content-Type": "application/json"}

responses_client = AsyncClient(app=app, base_url=TEST_BASE_URL)


async def start_quiz() -> Tuple[int, str]:
    response = await responses_client.post(
        "/api/quiz-start", json=QuizStartRequest(
            topic_id="73b445cc-34c6-482d-bf44-0db2f3a06e05",
            user_name="B",
            question_seconds=13
        ).to_dict(), headers=HEADER_JSON_CONTENT_TYPE)
    assert response.status_code == 200
    res_json = response.json()
    return res_json["state"]["quiz_code"], res_json["user"]["user_token"]
