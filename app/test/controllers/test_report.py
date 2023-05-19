import pytest
from app.controllers import IngredientController, ReportController, SizeController, BeverageController
from app.controllers.base import BaseController


def __get_item_ids(ingredients: list, beverages: list, size: dict):
    ingredients = [ingredient.get("_id") for ingredient in ingredients]
    beverages = [beverage.get("_id") for beverage in beverages]
    size_id = size.get("_id")
    return ingredients, beverages, size_id


def __create_items(items: list, controller: BaseController):
    created_items = []
    for item in items:
        created_item, _ = controller.create(item)
        created_items.append(created_item)
    return created_items


def __create_sizes_beverages_and_ingredients(ingredients: list, sizes: list, beverages: list):
    created_ingredients = __create_items(ingredients, IngredientController)
    created_sizes = __create_items(sizes, SizeController)
    created_beverages = __create_items(beverages, BeverageController)
    return created_sizes if len(created_sizes) > 1 else created_sizes.pop(), created_ingredients, created_beverages


def test_get_most_requested_ingredient(app, ingredients, size, clients_data, beverages, create_specific_orders):
    created_size, created_ingredients, created_beverages = __create_sizes_beverages_and_ingredients(
        ingredients, [size], beverages
    )
    ingredient_ids, beverage_ids, size_id = __get_item_ids(created_ingredients, created_beverages, created_size)
    expected_ingredient = created_ingredients[0]
    create_specific_orders(
        clients=clients_data,
        ingredients=ingredient_ids[:2],
        beverages=beverage_ids,
        sizes=[size_id],
        orders_len=3,
    )
    create_specific_orders(
        clients=clients_data,
        ingredients=ingredient_ids[:1],
        beverages=beverage_ids,
        sizes=[size_id],
        orders_len=2,
    )

    returned_report, _ = ReportController.get_all()

    actual_ingredient = returned_report["ingredient"]
    pytest.assume(expected_ingredient.get("_id") == actual_ingredient.get("_id"))


def test_get_month_with_more_revenue(app, ingredients, size, clients_data, beverages, create_specific_orders):
    created_size, created_ingredients, created_beverages = __create_sizes_beverages_and_ingredients(
        ingredients, [size], beverages
    )
    ingredient_ids, beverage_ids, size_id = __get_item_ids(created_ingredients, created_beverages, created_size)
    expected_month = 3
    create_specific_orders(
        clients=clients_data,
        ingredients=ingredient_ids[:1],
        beverages=beverage_ids,
        sizes=[size_id],
        orders_len=7,
        month=expected_month,
    )
    create_specific_orders(
        clients=clients_data,
        ingredients=ingredient_ids[:1],
        beverages=beverage_ids,
        sizes=[size_id],
        orders_len=2,
        month=2,
    )

    returned_report, _ = ReportController.get_all()

    actual_month = returned_report["month"]
    pytest.assume(expected_month == actual_month)


def test_get_top_customers(app, ingredients, size, clients_data, beverages, create_specific_orders):
    created_size, created_ingredients, created_beverages = __create_sizes_beverages_and_ingredients(
        ingredients, [size], beverages
    )
    ingredient_ids, beverage_ids, size_id = __get_item_ids(created_ingredients, created_beverages, created_size)
    expected_clients = set(client.get("client_name") for client in clients_data[:3])
    for i in range(len(expected_clients)):
        create_specific_orders(
            clients=[clients_data[i]],
            ingredients=ingredient_ids[:1],
            beverages=beverage_ids,
            sizes=[size_id],
            orders_len=5,
        )
    create_specific_orders(
        clients=clients_data,
        ingredients=ingredient_ids[:1],
        beverages=beverage_ids,
        sizes=[size_id],
        orders_len=5,
    )

    returned_report, _ = ReportController.get_all()

    actual_clients = set(returned_report["clients"])
    pytest.assume(not expected_clients.difference(actual_clients))
