from typing import Any, Optional, Sequence

from sqlalchemy.sql import text, column, func

from .models import Ingredient, Order, Size, Beverage, db, OrderDetail
from .serializers import IngredientSerializer, OrderSerializer, SizeSerializer, BeverageSerializer, ma


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def update(cls):
        raise NotImplementedError(f"Method not suported for {cls.__name__}")

    @classmethod
    def query_month_with_most_revenue(cls):
        query = (
            cls.session.query(
                func.strftime("%m", cls.model.date).label("month"), func.sum(cls.model.total_price).label("revenue")
            )
            .group_by(func.strftime("%m", cls.model.date))
            .order_by(func.sum(cls.model.total_price).desc())
        )

        return query.first()

    @classmethod
    def query_top_customers(cls, limit: int):
        query = (
            cls.session.query(cls.model.client_name)
            .group_by(cls.model.client_dni)
            .order_by(func.count().desc())
            .limit(limit)
        )
        return query.all()


class IndexManager(BaseManager):
    @classmethod
    def test_connection(cls):
        cls.session.query(column("1")).from_statement(text("SELECT 1")).all()


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class OrderDetailManager(BaseManager):
    model = OrderDetail

    @classmethod
    def query_most_requested_ingredient(cls):
        query = (
            cls.session.query(cls.model.ingredient_id).group_by(cls.model.ingredient_id).order_by(func.count().desc())
        )
        return query.first()
