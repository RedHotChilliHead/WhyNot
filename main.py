# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from time import monotonic
import asyncio
import uvicorn

app = FastAPI()
router = APIRouter()


class TestResponse(BaseModel):
    elapsed: float


lock = asyncio.Lock()


async def work() -> None:
    await asyncio.sleep(3)  # метод спит 3 секунды


@router.get("/test", response_model=TestResponse)  # предоставление метода GET /test
async def handler() -> TestResponse:
    ts1 = monotonic()
    async with lock:  # Не допускаем одновременной работы нескольких функций
        await work()
    ts2 = monotonic()
    return TestResponse(elapsed=ts2 - ts1)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # для запуска приложения uvicorn main:app --reload
