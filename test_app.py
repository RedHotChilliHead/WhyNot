import asyncio
import time
import httpx
import pytest


@pytest.mark.asyncio
async def test_concurrent_requests():
    start_time = time.monotonic()

    async def send_request():
        async with httpx.AsyncClient(timeout=10.0) as client:  # Тайм-аут до 10 секунд
            response = await client.get("http://127.0.0.1:8000/test")
            print(f"Полученный ответ: {response.json()}")
            return response

    # Отправляем несколько запросов одновременно с помощью asyncio.gather
    tasks = [send_request(), send_request(), send_request()]
    results = await asyncio.gather(*tasks)

    previous_elapsed = None
    for result in results:
        assert result.status_code == 200
        elapsed = result.json()["elapsed"]
        if previous_elapsed is not None:
            assert elapsed - previous_elapsed >= 3
        previous_elapsed = elapsed

    total_time = time.monotonic() - start_time
    print(f"Общее время выполнения теста: {total_time}")
