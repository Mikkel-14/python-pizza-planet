from typing import Optional

from .managers import BaseManager
from .models import Order, OrderDetail
from .serializers import OrderSerializer


class OrderDecorator(BaseManager):
    model = Order
    serializer = OrderSerializer
    manager: Optional[BaseManager] = None

    @classmethod
    def create(cls, entry: dict):
        raise NotImplementedError("Implement a concrete OrderDecorator!")

    @classmethod
    def update(cls):
        raise NotImplementedError(f"Method not suported for {cls.__name__}")

    @classmethod
    def set_manager(cls, manager: BaseManager):
        cls.manager = manager


class IngredientsOrderDecorator(OrderDecorator):
    @classmethod
    def create(cls, entry: dict):
        created_order = cls.manager.create(entry["order_data"])
        ingredients = entry["ingredients"]
        cls.session.add_all(
            (
                OrderDetail(
                    order_id=created_order["_id"], ingredient_id=ingredient._id, ingredient_price=ingredient.price
                )
                for ingredient in ingredients
            )
        )
        cls.session.commit()
        updated_order = cls.manager.get_by_id(created_order["_id"])
        return updated_order
