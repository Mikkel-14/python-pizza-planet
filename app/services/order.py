from app.common.http_methods import GET, POST
from flask import Blueprint, request

from ..controllers import OrderController
from .service_template import CreateService, GetByIdService, GetAllService

order = Blueprint("order", __name__)


@order.route("/", methods=POST)
def create_order():
    service = CreateService(OrderController)
    return service.run(request.json)


@order.route("/id/<_id>", methods=GET)
def get_order_by_id(_id: int):
    service = GetByIdService(OrderController)
    return service.run(_id)


@order.route("/", methods=GET)
def get_orders():
    service = GetAllService(OrderController)
    return service.run()
