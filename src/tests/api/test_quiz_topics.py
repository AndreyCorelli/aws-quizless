import pytest
from src.tests.api.api_test_client import responses_client


@pytest.mark.asyncio
async def test_quiz_topics():
    response = await responses_client.get(
        "/api/quiz-topics")
    assert response.status_code == 200
    print(response.json())
    res_json = response.json()
    assert len(res_json) == 2
