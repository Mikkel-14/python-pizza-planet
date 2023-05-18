from app.plugins import ma, db
from .models import Ingredient, Size, Order, OrderDetail, Beverage


class IngredientSerializer(ma.SQLAlchemyAutoSchema):
    class Meta(ma.SQLAlchemyAutoSchema.Meta):
        model = Ingredient
        sqla_session = db.session
        load_instance = True
        fields = ("_id", "name", "price")


class SizeSerializer(ma.SQLAlchemyAutoSchema):
    class Meta(ma.SQLAlchemyAutoSchema.Meta):
        model = Size
        sqla_session = db.session
        load_instance = True
        fields = ("_id", "name", "price")


class OrderDetailSerializer(ma.SQLAlchemyAutoSchema):
    ingredient = ma.Nested(IngredientSerializer)

    class Meta(ma.SQLAlchemyAutoSchema.Meta):
        model = OrderDetail
        sqla_session = db.session
        load_instance = True
        fields = ("ingredient_price", "ingredient")


class BeverageSerializer(ma.SQLAlchemyAutoSchema):
    class Meta(ma.SQLAlchemyAutoSchema.Meta):
        model = Beverage
        sqla_session = db.session
        load_instance = True
        fields = ("_id", "name", "price")


class OrderSerializer(ma.SQLAlchemyAutoSchema):
    size = ma.Nested(SizeSerializer)
    detail = ma.Nested(OrderDetailSerializer, many=True)
    beverages = ma.Nested(BeverageSerializer, many=True)

    class Meta(ma.SQLAlchemyAutoSchema.Meta):
        model = Order
        sqla_session = db.session
        load_instance = True
        fields = (
            "_id",
            "client_name",
            "client_dni",
            "client_address",
            "client_phone",
            "date",
            "total_price",
            "size",
            "size_id",
            "detail",
            "beverages",
        )
