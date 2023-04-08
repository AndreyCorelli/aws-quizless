from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.api import api_router

app = FastAPI(
    title="Quizless",
    servers=[
        {
            "url": "http://localhost:{port}",
            "description": "local",
            "variable": {"port": {"default": 8055}}
        }
    ]
)

app.include_router(api_router, prefix="/api")


async def handle_global_exception(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        return JSONResponse({"internal_error": str(exc)}, status_code=500)


app.middleware("http")(handle_global_exception)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8055, reload=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
