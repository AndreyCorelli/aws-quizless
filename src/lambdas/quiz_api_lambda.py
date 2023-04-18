import json
from typing import Dict, Any

from domain.quiz_manager import quiz_manager
from domain.quiz_requests import QuizStartRequest, QuizJoinRequest, ScheduleQuizRequest, QuizStatusRequest, \
    StoreAnswerRequest, QuizResultsRequest
from settings import settings


def get_topics(_request_data: Dict[str, Any]) -> str:
    topics = quiz_manager.get_quiz_topics()
    return json.dumps([
        t.to_dict() for t in topics
    ])


def start_quiz(request_data: Dict[str, Any]) -> str:
    res = quiz_manager.start_quiz(QuizStartRequest.from_dict(request_data))
    ret_value = res.to_json()
    return ret_value


def join_quiz(request_data: Dict[str, Any]) -> str:
    res = quiz_manager.join_quiz(QuizJoinRequest.from_dict(request_data))
    ret_value = res.to_json()
    return ret_value


def schedule_quiz(request_data: Dict[str, Any]) -> str:
    res = quiz_manager.schedule_quiz(ScheduleQuizRequest.from_dict(request_data))
    ret_value = res.to_json()
    return ret_value


def get_quiz_state(request_data: Dict[str, Any]) -> str:
    res = quiz_manager.get_quiz_state(QuizStatusRequest.from_dict(request_data))
    ret_value = res.to_json()
    return ret_value


def answer_quiz(request_data: Dict[str, Any]) -> str:
    res = quiz_manager.store_answer(StoreAnswerRequest.from_dict(request_data))
    ret_value = res.to_json()
    return ret_value


def get_quiz_results(request_data: Dict[str, Any]) -> str:
    res = quiz_manager.get_quiz_results(QuizResultsRequest.from_dict(request_data).quiz_code)
    if res:
        return res.to_json()
    return ""


function_by_request = {
    "quiz-topics": get_topics,
    "quiz-start": start_quiz,
    "quiz-join": join_quiz,
    "quiz-schedule": schedule_quiz,
    "quiz-check-status": get_quiz_state,
    "quiz-answer": answer_quiz,
    "quiz-results": get_quiz_results
}


def lambda_handler(event: Dict[str, Any], context=None) -> Dict[str, Any]:
    try:
        event_data = json.loads(event["body"])
        if "requested_operation" not in event_data:
            raise Exception("The payload should contain \"requested_operation\" field")
        if event_data["requested_operation"] not in function_by_request:
            raise Exception("The \"requested_operation\" value is incorrect. "
                            "The correct options are: " +
                            ", ".join(function_by_request.keys()))

        processor = function_by_request[event_data["requested_operation"]]
        response_data = processor(event_data.get("payload"))
        return {
            "statusCode": 200,
            "body": response_data,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': settings.allowed_origins,
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
        }
    except Exception as e:
        error_str = str(e)
        body_str = json.dumps({"exception": error_str})
        return {
            "statusCode": 500,
            "body": body_str,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': settings.allowed_origins,
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
        }


if __name__ == "__main__":
    result = lambda_handler({
        "body": json.dumps({
            "requested_operation": "quiz-results",
            "payload": {
                "quiz_code": 123123
            }
        })
    })
    print(result)
