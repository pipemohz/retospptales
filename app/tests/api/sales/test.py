import pytest
from app.api import create_app


app = create_app('default')
ENDPOINT = '/api/v1/sales'


@pytest.fixture
def set_valid_query():
    with app.test_client() as c:
        response = c.get(f'{ENDPOINT}?id=42787138')
    yield response


@pytest.fixture
def set_empty():
    with app.test_client() as c:
        response = c.get(f'{ENDPOINT}?id=12345')
    yield response


@pytest.fixture
def set_invalid_query():

    queries = [
        'id=42787138&year=2022a&month11',
        'id=42787138&year=2022&month11s',
        'id=test&year=2022&month11'
    ]
    responses = list()
    with app.test_client() as c:
        for q in queries:
            responses.append(c.get(f'{ENDPOINT}?{q}'))
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


def test_invalid_query_parameters(set_invalid_query):
    responses = set_invalid_query
    assert all(
        [True if r.status_code == 400 else False for r in responses])
