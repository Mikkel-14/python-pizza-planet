from typing import List

from faker import Faker

from ..controllers.order import OrderController
from ..test.fixtures.order import client_data_mock
from ..test.utils.functions import shuffle_list


class OrderGenerator:
    def __init__(self) -> None:
        self.orders: List = None

    def generate(self, ingredients, beverages, sizes):
        if not self.orders:
            client_data = self._generate_client_data()
            ingredient_ids = [ingredient._id for ingredient in ingredients]
            beverage_ids = [beverage._id for beverage in beverages]
            size_ids = [size._id for size in sizes]
            self._compose_orders(
                client_data,
                ingredient_ids,
                beverage_ids,
                size_ids,
            )

        return self.orders

    def _generate_client_data(self):
        client_data = []
        for _ in range(10):
            client_datum = client_data_mock()
            client_data.append(client_datum)
        return client_data

    def _compose_orders(self, client_data, ingredients, beverages, sizes):
        self.orders = []
        for _ in range(100):
            order = {
                **shuffle_list(client_data)[0],
                "ingredients": shuffle_list(ingredients)[:5],
                "beverages": shuffle_list(beverages)[:5],
                "size_id": shuffle_list(sizes)[0],
                "date": Faker().date_time_between(start_date="-11M", end_date="-1M").isoformat(),
            }
            self.orders.append(order)


class OrderSeeder:
    def run(self, ingredients, beverages, sizes):
        serialized_orders = OrderGenerator().generate(ingredients, beverages, sizes)
        for order in serialized_orders:
            OrderController.create(order)
