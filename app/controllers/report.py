from typing import Any, Optional, Tuple

from sqlalchemy.exc import SQLAlchemyError

from .base import BaseController
from ..repositories.managers import IngredientManager, OrderDetailManager, OrderManager


class ReportController(BaseController):
    ingredient_manager = IngredientManager
    order_detail_manager = OrderDetailManager
    order_manager = OrderManager

    @classmethod
    def get_all(cls) -> Tuple[Any, Optional[str]]:
        try:
            ingredient = cls._get_most_requested_ingredient()
            month_and_revenue = cls._get_month_with_most_revenue()
            response = cls._construct_response(ingredient, month_and_revenue)
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
        data = OrderManager.query_month_with_most_revenue()
        return data

    @classmethod
    def _construct_response(cls, ingredient: dict, month_and_revenue: dict):
        response = {
            "ingredient": ingredient,
            "month": int(month_and_revenue["month"]),
            "revenue": month_and_revenue["revenue"],
        }
        return response
