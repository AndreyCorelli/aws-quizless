from typing import Union, List, Dict, Any

from fastapi import APIRouter

from domain.quiz_manager import quiz_manager
from domain.quiz_requests import QuizStartRequest, QuizJoinRequest, ScheduleQuizRequest, QuizStatusRequest, \
    StoreAnswerRequest

route = APIRouter()


@route.get("/quiz-topics")
async def get_topics() -> List[Dict[str, Any]]:
    topics = quiz_manager.get_quiz_topics()
    return [
        t.to_dict() for t in topics
    ]


@route.post("/quiz-start")
async def start_quiz(request_data: QuizStartRequest) -> Dict[str, Any]:
    res = quiz_manager.start_quiz(request_data)
    ret_value = res.to_dict()
    return ret_value


@route.post("/quiz-join")
async def join_quiz(request_data: QuizJoinRequest) -> Dict[str, Any]:
    res = quiz_manager.join_quiz(request_data)
    ret_value = res.to_dict()
    return ret_value


@route.post("/quiz-schedule")
async def schedule_quiz(request_data: ScheduleQuizRequest) -> Dict[str, Any]:
    res = quiz_manager.schedule_quiz(request_data)
    ret_value = res.to_dict()
    return ret_value


@route.post("/quiz-check-status")
async def get_quiz_state(request_data: QuizStatusRequest) -> Dict[str, Any]:
    res = quiz_manager.get_quiz_state(request_data)
    ret_value = res.to_dict()
    return ret_value


@route.post("/quiz-answer")
async def answer_quiz(request_data: StoreAnswerRequest) -> Dict[str, Any]:
    res = quiz_manager.store_answer(request_data)
    ret_value = res.to_dict()
    return ret_value


@route.get("/quiz-results/{quiz_code}")
async def get_quiz_results(quiz_code: int) -> Dict[str, Any]:
    res = quiz_manager.get_quiz_results(quiz_code)
    if res:
        res = {"quiz_results": res[0], "quiz_data": res[1]}
    return res
