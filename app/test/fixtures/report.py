from datetime import datetime
import pytest

from app.test.utils.functions import shuffle_list, get_random_day


@pytest.fixture
def create_specific_orders(client, order_uri):
    def __create_orders_factory(**kwargs):
        clients = kwargs.get("clients", [])
        ingredients = kwargs.get("ingredients", [])
        beverages = kwargs.get("beverages", [])
        sizes = kwargs.get("sizes", [])
        orders_len = kwargs.get("orders_len", 5)
        orders_month = kwargs.get("month", 1)
        current_year = datetime.now().year
        orders = []
        for _ in range(orders_len):
            order_day = get_random_day()
            new_order = client.post(
                order_uri,
                json={
                    **shuffle_list(clients)[0],
                    "ingredients": shuffle_list(ingredients)[: len(ingredients)],
                    "beverages": shuffle_list(beverages)[: len(beverages)],
                    "size_id": shuffle_list(sizes)[0],
                    "date": datetime(current_year, orders_month, order_day).isoformat(),
                },
            )
            orders.append(new_order)
        return orders

    return __create_orders_factory
