import os
from typing import List

from src.domain.quiz_data import QuizData
from src.settings import settings


class QuizMetadataRepository:
    def read_quizes(self) -> List[QuizData]:
        quizes: List[QuizData] = []
        quiz_path = settings.quiz_path
        for dir_name, dir_path in [
            (o, os.path.join(quiz_path, o)) for o in os.listdir(quiz_path)
            if os.path.isdir(os.path.join(quiz_path, o))
        ]:
            # check if the dir_name var contains UUID4
            quiz = self._read_quiz_from_path(dir_path)
            quizes.append(quiz)
        return quizes

    def _read_quiz_from_path(self, quiz_path: str) -> QuizData:
        file_path = os.path.join(quiz_path, "quiz_data.json")
        with open(file_path, "r") as file:
            json_str = file.read()
        quiz_data = QuizData.from_json(json_str, infer_missing=True)
        return quiz_data
