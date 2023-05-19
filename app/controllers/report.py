from typing import Any, Optional, Tuple

from sqlalchemy.exc import SQLAlchemyError

from .base import BaseController
from ..repositories.managers import IngredientManager, OrderDetailManager, OrderManager


class ReportController(BaseController):
    ingredient_manager = IngredientManager
    order_detail_manager = OrderDetailManager
    order_manager = OrderManager
    TOP_CUSTOMERS_LIMIT = 3

    @classmethod
    def get_all(cls) -> Tuple[Any, Optional[str]]:
        try:
            ingredient = cls._get_most_requested_ingredient()
            month_and_revenue = cls._get_month_with_most_revenue()
            customer_names = cls._get_top_customers()
            response = cls._construct_response(ingredient, month_and_revenue, customer_names)
            return response, None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)

    @classmethod
    def _get_most_requested_ingredient(cls):
        ingredient_id = OrderDetailManager.query_most_requested_ingredient()
        ingredient = IngredientManager.get_by_id(ingredient_id)
        return ingredient

    @classmethod
    def _get_month_with_most_revenue(cls):
        month_and_revenue = OrderManager.query_month_with_most_revenue()
        return month_and_revenue

    @classmethod
    def _get_top_customers(cls):
        customer_names = OrderManager.query_top_customers(cls.TOP_CUSTOMERS_LIMIT)
        return customer_names

    @classmethod
    def _construct_response(cls, ingredient: dict, month_and_revenue: dict, customer_names: list):
        response = {
            "ingredient": ingredient,
            "month": int(month_and_revenue["month"]),
            "revenue": round(month_and_revenue["revenue"], 2),
            "clients": list(map(lambda tuple_element: tuple_element[0], customer_names)),
        }
        return response
