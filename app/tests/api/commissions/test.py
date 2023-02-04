import pytest
from app.api import create_app


app = create_app('default')
ENDPOINT = '/api/v1/commissions'
body = {
    "id": "71695419",
    "products": [
        {
            "code": "1",
            "value": 10000
        },
        {
            "code": "2",
            "value": "10000"
        },
        {
            "code": 3,
            "value": "10000"
        }

    ]
}


@pytest.fixture
def set_valid_query():
    with app.test_client() as c:
        response = c.post(ENDPOINT, json=body)
    yield response


@pytest.fixture
def set_empty():
    body["id"] = '11357'
    with app.test_client() as c:
        response = c.post(ENDPOINT, json=body)
    yield response


@pytest.fixture
def set_invalid_products():

    products = [
        {
            'code': '1a',
            'value': 1000
        },
        {
            'code': '1',
            'value': '1000a'
        },
        {
            'code': 1,
            'value': 1000,
            'extra': 'value'
        }

    ]
    responses = list()
    with app.test_client() as c:
        for p in products:
            bad_body = body
            bad_body['products'] = p
            responses.append(c.post(ENDPOINT, json=bad_body))
    yield responses


def test_valid_response(set_valid_query):
    response = set_valid_query
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_empty_response(set_empty):
    response = set_empty
    assert response.status_code == 404
    assert response.content_type == 'application/json'
    assert response.json['data'] == []


def test_invalid_body_products(set_invalid_products):
    responses = set_invalid_products
    assert all(
        [True if r.status_code == 400 else False for r in responses])
