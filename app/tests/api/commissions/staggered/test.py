import pytest
from app.api import create_app
import asyncio

app = create_app('default')

ENDPOINT = '/api/v1/staggered'
body = {
    "id": "588372",
    "products": [
        {
            "code": "1",
            "value": "2000000"
        },
        {
            "code": "2",
            "value": "53723"
        },
        {
            "code": "3",
            "value": "156302"
        },
        {
            "code": "4",
            "value": "50420"
        },
        {
            "code": "150",
            "value": "88235"
        },
        {
            "code": "183",
            "value": "54626"
        },
        {
            "code": "303",
            "value": "407594"
        },
        {
            "code": "357",
            "value": "37818"
        },
        {
            "code": "401",
            "value": "112627"
        }
    ],
    "month": "11",
    "year": 2022
}


@pytest.mark.asyncio
async def test_concurrent_requests():
    def sync_test():
        with app.test_client() as client:
            response = client.post(ENDPOINT, json=body)
            assert response.status_code == 200
            # assert response.json['data']['commission'] == "138066.60000"

    loop = asyncio.get_running_loop()
    for _ in range(10):
        await loop.run_in_executor(None, sync_test)
