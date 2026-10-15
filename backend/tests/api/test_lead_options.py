from httpx import AsyncClient


async def test_lists_interest_options(client: AsyncClient) -> None:
    response = await client.get("/api/v1/lead/options")

    assert response.status_code == 200
    assert response.json() == [
        {"value": "subscription", "label": "Подписка"},
        {"value": "one_time", "label": "Разовый заказ"},
        {"value": "question", "label": "Вопрос"},
    ]
