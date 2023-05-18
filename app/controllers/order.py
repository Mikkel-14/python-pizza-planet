from sqlalchemy.exc import SQLAlchemyError

from ..common.utils import check_required_keys
from ..repositories.managers import IngredientManager, OrderManager, SizeManager, BeverageManager
from ..repositories.decorators import IngredientsOrderDecorator, BeveragesOrderDecorator
from .base import BaseController


class OrderController(BaseController):
    manager = OrderManager
    __required_info = ("client_name", "client_dni", "client_address", "client_phone", "size_id")

    @staticmethod
    def calculate_order_price(size_price: float, ingredients_and_beverages: dict) -> float:
        price = (
            sum(ingredient.price for ingredient in ingredients_and_beverages["ingredients"])
            + size_price
            + sum(beverage.price for beverage in ingredients_and_beverages["beverages"])
        )
        return round(price, 2)

    @classmethod
    def create(cls, order: dict):
        current_order = order.copy()
        cls._get_decorated_order_manager()
        if not check_required_keys(cls.__required_info, current_order):
            return None, "Invalid order payload"

        size_id = current_order.get("size_id")
        size = SizeManager.get_by_id(size_id)

        if not size:
            return (
                None,
                "Invalid size for Order",
            )

        ingredient_ids = current_order.pop("ingredients", [])
        beverage_ids = current_order.pop("beverages", [])
        try:
            ingredients = IngredientManager.get_by_id_list(ingredient_ids)
            beverages = BeverageManager.get_by_id_list(beverage_ids)
            ingredients_and_beverages = {"ingredients": ingredients, "beverages": beverages}
            price = cls.calculate_order_price(size.get("price"), ingredients_and_beverages)
            order_with_price = {**current_order, "total_price": price}
            order_with_ingredients_and_beverages = {**order_with_price, **ingredients_and_beverages}
            return cls.manager.create(order_with_ingredients_and_beverages), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)

    @classmethod
    def _get_decorated_order_manager(cls):
        beverage_decorated_manager = BeveragesOrderDecorator
        ingredient_decorated_manager = IngredientsOrderDecorator

        ingredient_decorated_manager.manager = OrderManager
        beverage_decorated_manager.manager = ingredient_decorated_manager
        cls.manager = beverage_decorated_manager
