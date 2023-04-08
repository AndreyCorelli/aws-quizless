import copy
import math
from typing import Tuple, List

from src.domain.constants import QuizConstants
from src.domain.quiz_data import QuizData
from src.domain.quiz_state import QuizState, QuizPlayers, QuizStatusCode, QuizResults, QuizResultsPlayer
from src.domain.repository.quiz_state_repository import QuizStateRepository
from src.utils import get_utc_now_time


class QuizStateUpdateManager:
    def __init__(self, state_repo: QuizStateRepository, quizes: List[QuizData]):
        self._state_repo = state_repo
        self._quizes: List[QuizData] = quizes

    def read_and_update_quiz_state(self, quiz_code: int) -> Tuple[QuizState, QuizPlayers]:
        q_state, players = self._state_repo.read_quiz_state(quiz_code)
        self._update_quiz_state(q_state)
        return q_state, players

    def _update_quiz_state(self, q_state: QuizState) -> None:
        tm = get_utc_now_time()

        if q_state.status == QuizStatusCode.PENDING:
            if q_state.expiration > tm:
                q_state.updates_in_seconds = math.ceil((q_state.expiration - tm).total_seconds())
            return

        if q_state.status == QuizStatusCode.SCHEDULED:
            if q_state.starts_at > tm:
                q_state.updates_in_seconds = math.ceil((q_state.expiration - tm).total_seconds())
            else:
                q_state.status = QuizStatusCode.STARTED
                self._state_repo.set_state(q_state, QuizConstants.STARTED_QUIZ_EXPIRATION_SECONDS)

        self._check_and_update_running_quiz(q_state)

    def _check_and_update_running_quiz(self, q_state: QuizState) -> None:
        if q_state.status != QuizStatusCode.STARTED:
            return
        quiz_data = [q for q in self._quizes if q.id == q_state.id][0]
        seconds_since_started = (get_utc_now_time() - q_state.starts_at).total_seconds()
        question_index = math.floor(seconds_since_started / q_state.question_seconds)
        q_state.updates_in_seconds = q_state.question_seconds - math.floor(
            seconds_since_started % q_state.question_seconds)
        if question_index >= len(quiz_data.questions):
            self._finish_quiz(q_state)
        else:
            if q_state.cur_question_index[0] != question_index:
                q_state.cur_question_index = question_index, len(quiz_data.questions)
                q_state.cur_question = copy.deepcopy(quiz_data.questions[question_index])
                q_state.cur_question.correct_answers = []
                self._state_repo.set_state(q_state, QuizConstants.STARTED_QUIZ_EXPIRATION_SECONDS)

    def _finish_quiz(self, q_state: QuizState) -> None:
        if q_state.status == QuizStatusCode.FINISHED:
            return
        q_state.status = QuizStatusCode.FINISHED

        quiz_data = [q for q in self._quizes if q.id == q_state.id][0]
        players = self._state_repo.read_quiz_players(q_state.quiz_code)

        player_scores: List[Tuple[int, int]] = [(0, 0)] * len(players.players)
        for i, question in enumerate(quiz_data.questions):
            sorted_answers = sorted(question.correct_answers)

            for player_index, player in enumerate(players.players):
                if i >= len(player.answers):
                    continue
                score = player_scores[player_index]
                player_answering_time = player.answers[i].answer_given_seconds
                if player_answering_time < 0:
                    player_answering_time = q_state.question_seconds
                player_answers = sorted(player.answers[i].answer)
                if sorted_answers == player_answers:
                    score = score[0] + 1, score[1]
                score = score[0], score[1] + player_answering_time
                player_scores[player_index] = score

        player_scores_index = [(i, score) for i, score in enumerate(player_scores)]
        player_scores_index.sort(key=lambda item: (item[1][0], -item[1][1]), reverse=True)

        results = QuizResults(
            quiz_id=q_state.id,
            quiz_name=q_state.name,
            started_at=q_state.starts_at,
            players=[]
        )

        for index, score in player_scores_index:
            player_score = QuizResultsPlayer(
                name=players.players[index].name,
                correct_answers=score[0],
                total_answering_time=score[1],
                answers=players.players[index].answers
            )
            results.players.append(player_score)

        self._state_repo.set_quiz_results(
            q_state.quiz_code, results, QuizConstants.STARTED_QUIZ_EXPIRATION_SECONDS)
