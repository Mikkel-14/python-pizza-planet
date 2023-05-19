from typing import Any, Optional, Tuple

from sqlalchemy.exc import SQLAlchemyError

from .base import BaseController
from ..repositories.managers import IngredientManager, OrderDetailManager


class ReportController(BaseController):
    ingredient_manager = IngredientManager
    order_detail_manager = OrderDetailManager

    @classmethod
    def get_all(cls) -> Tuple[Any, Optional[str]]:
        try:
            ingredient = cls._get_most_requested_ingredient()
            response = cls._construct_response(ingredient)
            return response, None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)

    @classmethod
    def _get_most_requested_ingredient(cls):
        ingredient_id = OrderDetailManager.query_most_requested_ingredient()
        ingredient = IngredientManager.get_by_id(ingredient_id)
        return ingredient

    @classmethod
    def _construct_response(cls, ingredient: dict):
        response = {"ingredient": ingredient}
        return response
