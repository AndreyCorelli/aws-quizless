from typing import List

from domain.quiz_data import QuizData


class BaseQuizMetadataRepository:
    def read_quizes(self) -> List[QuizData]:
        raise NotImplementedError()
