import datetime
import random
import uuid
from typing import List, Tuple, Optional

from src.domain.constants import QuizConstants
from src.domain.quiz_data import QuizData
from src.domain.quiz_requests import QuizStartRequest, QuizJoinRequest, ScheduleQuizRequest, QuizStatusRequest, \
    StoreAnswerRequest
from src.domain.quiz_state import UserQuizState, QuizState, QuizStatusCode, QuizPlayer, QuizUserRole, QuizPlayers, \
    QuizPlayerAnswer, QuizResults
from src.domain.quiz_state_update_manager import QuizStateUpdateManager
from src.domain.quiz_topic import QuizTopic
from src.domain.repository.quiz_metadata_repository import QuizMetadataRepository
from src.domain.repository.quiz_state_repository import QuizStateRepository
from src.utils import get_utc_now_time


class QuizManager:
    def __init__(self):
        self._quizes: List[QuizData] = QuizMetadataRepository().read_quizes()
        self._state_repo = QuizStateRepository()
        self._state_update_manager = QuizStateUpdateManager(self._state_repo, self._quizes)

    def get_quiz_topics(self) -> List[QuizTopic]:
        return [
            QuizTopic(id=q.id, name=q.name) for q in self._quizes
        ]

    def start_quiz(self, request_data: QuizStartRequest) -> UserQuizState:
        quizes = [q for q in self._quizes if q.id == request_data.topic_id]
        if not quizes:
            raise Exception(f"Quiz #{request_data.topic_id} wasn't found out ouf "
                            f"{self._quizes} quizes")
        quiz = quizes[0]
        expires_at = get_utc_now_time() + datetime.timedelta(
            seconds=QuizConstants.PENDING_QUIZ_EXPIRATION_SECONDS)
        state = QuizState(
            id=quiz.id,
            name=quiz.name,
            quiz_code=random.randint(0, 100000),
            status=QuizStatusCode.PENDING,
            expiration=expires_at,
            starts_at=None,
            question_seconds=request_data.question_seconds,
        )
        self._state_repo.set_state(state, QuizConstants.PENDING_QUIZ_EXPIRATION_SECONDS)

        player_data = QuizPlayer(
            user_token=str(uuid.uuid4()),
            name=request_data.user_name,
            user_role=QuizUserRole.COMMANDER,
            answers=[]
        )
        quiz_user_data = UserQuizState(
            state=state,
            user=player_data,
            all_user_names=[player_data.name]
        )

        self._state_repo.set_quiz_players(
            state.quiz_code, QuizPlayers(players=[player_data]),
            QuizConstants.PENDING_QUIZ_EXPIRATION_SECONDS)
        return quiz_user_data

    def join_quiz(self, request_data: QuizJoinRequest) -> UserQuizState:
        q_state, quiz_players = self._state_update_manager.read_and_update_quiz_state(
            request_data.quiz_code
        )
        if request_data.user_name in {p.name for p in quiz_players.players}:
            raise Exception(f"User name {request_data.user_name} is already occupied")
        quiz_players.players.append(QuizPlayer(
            user_token=str(uuid.uuid4()),
            name=request_data.user_name,
            user_role=QuizUserRole.PLAYER,
            answers=[]
        ))
        self._state_repo.set_quiz_players(
            request_data.quiz_code, quiz_players,
            QuizConstants.PENDING_QUIZ_EXPIRATION_SECONDS)
        quiz_user_data = UserQuizState(
            state=q_state,
            user=quiz_players.players[-1],
            all_user_names=[p.name for p in quiz_players.players]
        )
        return quiz_user_data

    def schedule_quiz(self, request_data: ScheduleQuizRequest) -> UserQuizState:
        q_state, quiz_players = self._state_update_manager.read_and_update_quiz_state(
            request_data.quiz_code
        )
        current_users = [p for p in quiz_players.players if p.user_token == request_data.user_token]
        if not current_users:
            raise Exception("User token not found among the quiz users")

        if current_users[0].user_role != QuizUserRole.COMMANDER:
            raise Exception("Current user is not a quiz commander")
        # update the quiz state
        q_state.status = QuizStatusCode.SCHEDULED
        q_state.starts_at = get_utc_now_time() + datetime.timedelta(
            seconds=request_data.delay_seconds)
        q_state.updates_in_seconds = request_data.delay_seconds
        self._state_repo.set_state(
            q_state,
            QuizConstants.STARTED_QUIZ_EXPIRATION_SECONDS + request_data.delay_seconds
        )
        quiz_user_data = UserQuizState(
            state=q_state,
            user=current_users[0],
            all_user_names=[p.name for p in quiz_players.players]
        )
        return quiz_user_data

    def get_quiz_state(self, request_data: QuizStatusRequest) -> UserQuizState:
        q_state, quiz_players = self._state_update_manager.read_and_update_quiz_state(
            request_data.quiz_code
        )
        current_users = [p for p in quiz_players.players if p.user_token == request_data.user_token]
        quiz_user_data = UserQuizState(
            state=q_state,
            user=current_users[0],
            all_user_names=[p.name for p in quiz_players.players]
        )
        return quiz_user_data

    def store_answer(self, request_data: StoreAnswerRequest) -> UserQuizState:
        answer_time = get_utc_now_time()
        q_state, quiz_players = self._state_update_manager.read_and_update_quiz_state(
            request_data.quiz_code
        )
        if q_state.status != QuizStatusCode.STARTED:
            raise Exception(f"Quiz {request_data.quiz_code} is in {q_state.status} status")

        current_users = [p for p in quiz_players.players if p.user_token == request_data.user_token]
        if not current_users:
            raise Exception("User token not found among the quiz users")

        if request_data.question_index != q_state.cur_question_index[0]:
            raise Exception(f"Current question index is {request_data.question_index}, "
                            f"but the current quiz question is {q_state.cur_question_index}")

        if not current_users[0].answers:
            current_users[0].answers = [QuizPlayerAnswer(
                answer=[]
            )] * q_state.cur_question_index[1]

        seconds_since_started = (answer_time - q_state.starts_at).total_seconds()
        time_passed = round(seconds_since_started % q_state.question_seconds)
        current_users[0].answers[request_data.question_index] = QuizPlayerAnswer(
            answer=request_data.answer,
            answer_given_seconds=time_passed
        )
        self._state_repo.set_quiz_players(
            request_data.quiz_code, quiz_players,
            QuizConstants.STARTED_QUIZ_EXPIRATION_SECONDS)
        quiz_user_data = UserQuizState(
            state=q_state,
            user=current_users[0],
            all_user_names=[p.name for p in quiz_players.players]
        )
        return quiz_user_data

    def get_quiz_results(self, quiz_code: int) -> Optional[Tuple[QuizResults, QuizData]]:
        results = self._state_repo.read_quiz_results(quiz_code)
        if not results:
            return None
        quiz_data = [q for q in self._quizes if q.id == results.quiz_id][0]
        return results, quiz_data


quiz_manager = QuizManager()
