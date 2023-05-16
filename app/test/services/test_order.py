import pytest


def test_create_order_service(create_order):
    new_order = create_order
    pytest.assume(new_order.status.startswith('200'))
    created_order = new_order.json
    pytest.assume(created_order['_id'])
    pytest.assume(created_order['client_address'])
    pytest.assume(created_order['client_dni'])
    pytest.assume(created_order['client_name'])
    pytest.assume(created_order['client_phone'])
    pytest.assume(created_order['date'])
    pytest.assume(created_order['detail'])
    pytest.assume(created_order['size'])


def test_get_order_by_id_service(client, order_uri, create_order):
    current_order = create_order.json
    response = client.get(f'{order_uri}id/{current_order["_id"]}')
    pytest.assume(response.status.startswith('200'))
    returned_order = response.json
    for param, value in current_order.items():
        pytest.assume(returned_order[param] == value)


def test_get_orders_service(client, order_uri, create_orders):
    current_orders = list(map
                          (
                            lambda order_response: order_response.json,
                            create_orders
                          ))
    response = client.get(order_uri)
    pytest.assume(response.status.startswith('200'))
    returned_orders = response.json
    pytest.assume(current_orders == returned_orders)
