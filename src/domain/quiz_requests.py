from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class QuizStartRequest:
    topic_id: str
    user_name: str
    question_seconds: int = 10


@dataclass_json
@dataclass
class QuizJoinRequest:
    quiz_code: int
    user_name: str


@dataclass_json
@dataclass
class ScheduleQuizRequest:
    quiz_code: int
    user_token: str
    delay_seconds: int


@dataclass_json
@dataclass
class QuizStatusRequest:
    quiz_code: int
    user_token: str


@dataclass_json
@dataclass
class StoreAnswerRequest:
    quiz_code: int
    user_token: str
    answer: List[int]
    question_index: int
