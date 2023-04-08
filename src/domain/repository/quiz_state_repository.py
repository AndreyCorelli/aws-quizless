import datetime
import random
from typing import Tuple

import redis

from src.domain.constants import QuizConstants
from src.domain.quiz_state import QuizState, QuizStatusCode, QuizPlayers, QuizResults
from src.settings import settings
from src.utils import get_utc_now_time


class QuizStateRepository:
    def __init__(self):
        self.redis_cli = redis.Redis(host=settings.redis_host, port=settings.redis_port)

    def set_state(self, q_state: QuizState, expiration_seconds: int) -> None:
        self.redis_cli.set(
            f"quiz_{q_state.quiz_code}",
            q_state.to_json(),
            ex=expiration_seconds or None
        )

    def set_quiz_players(self, quiz_code: int, quiz_players: QuizPlayers,
                         expiration_seconds: int) -> None:
        self.redis_cli.set(
            f"quiz_players_{quiz_code}",
            quiz_players.to_json(),
            ex=expiration_seconds or None
        )

    def set_quiz_results(self, quiz_code: int, quiz_results: QuizResults,
                         expiration_seconds: int) -> None:
        self.redis_cli.set(
            f"quiz_results_{quiz_code}",
            quiz_results.to_json(),
            ex=expiration_seconds or None
        )

    def read_quiz_state(self, quiz_code: int) -> Tuple[QuizState, QuizPlayers]:
        json_data = self.redis_cli.get(f"quiz_{quiz_code}")
        if not json_data:
            raise Exception(f"Quiz #{quiz_code} not found")
        q_state: QuizState = QuizState.from_json(json_data)
        players = self.read_quiz_players(quiz_code)
        return q_state, players

    def read_quiz_players(self, quiz_code: int) -> QuizPlayers:
        json_data = self.redis_cli.get(f"quiz_players_{quiz_code}")
        if not json_data:
            raise Exception(f"Quiz #{quiz_code} not found while reading quiz players")
        players: QuizPlayers = QuizPlayers.from_json(json_data)
        return players

    def read_quiz_results(self, quiz_code: int) -> QuizResults:
        json_data = self.redis_cli.get(f"quiz_results_{quiz_code}")
        if not json_data:
            raise Exception(f"Quiz #{quiz_code} not found while reading quiz players")
        results: QuizResults = QuizResults.from_json(json_data)
        return results
