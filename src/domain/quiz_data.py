import enum
from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from domain.quiz_topic import QuizTopic


class QuizQuestionType(enum.Enum):
    SINGLE_CHOICE = "SINGLE_CHOICE"
    MULTI_CHOICE = "MULTI_CHOICE"


@dataclass_json
@dataclass
class QuizQuestion:
    image: str
    text: str
    answers: List[str]
    correct_answers: List[int]
    question_type: QuizQuestionType


@dataclass_json
@dataclass
class QuizData(QuizTopic):
    questions: List[QuizQuestion]
