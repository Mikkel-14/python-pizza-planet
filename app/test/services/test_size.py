import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_create_size_service(create_size):
    size = create_size.json
    pytest.assume(create_size.status.startswith('200'))
    pytest.assume(size['name'])
    pytest.assume(size['price'])


def test_update_size_service(client, create_size, size_uri):
    size = create_size.json
    modified_size = {**size, 'name': get_random_string(), 'price': get_random_price(1, 5)}
    response = client.put(size_uri, json=modified_size)
    pytest.assume(response.status.startswith('200'))
    updated_size = response.json
    for param, value in modified_size.items():
        pytest.assume(updated_size[param] == value)


def test_get_size_by_id(client, create_size, size_uri):
    current_size = create_size.json
    response = client.get(f'{size_uri}id/{current_size["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_size = response.json
    for param, value in current_size.items():
        pytest.assume(returned_size[param] == value)
