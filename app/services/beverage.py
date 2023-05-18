from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import BeverageController
from .service_template import CreateService, UpdateService, GetByIdService, GetAllService

beverage = Blueprint("beverage", __name__)


@beverage.route("/", methods=POST)
def create_beverage():
    service = CreateService(BeverageController)
    return service.run(request.json)


@beverage.route("/", methods=PUT)
def update_beverage():
    service = UpdateService(BeverageController)
    return service.run(request.json)


@beverage.route("/id/<_id>", methods=GET)
def get_beverage_by_id(_id: int):
    service = GetByIdService(BeverageController)
    return service.run(_id)


@beverage.route("/", methods=GET)
def get_beverages():
    service = GetAllService(BeverageController)
    return service.run()
