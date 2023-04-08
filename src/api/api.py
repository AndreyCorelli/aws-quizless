from fastapi import APIRouter

from src.api.endpoints import quiz


api_router = APIRouter()
api_router.include_router(quiz.route, tags=["quiz"])
