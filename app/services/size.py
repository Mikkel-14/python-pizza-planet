from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import SizeController
from .service_template import CreateService, UpdateService, GetByIdService, GetAllService

size = Blueprint("size", __name__)


@size.route("/", methods=POST)
def create_size():
    service = CreateService(SizeController)
    return service.run(request.json)


@size.route("/", methods=PUT)
def update_size():
    service = UpdateService(SizeController)
    return service.run(request.json)


@size.route("/id/<_id>", methods=GET)
def get_size_by_id(_id: int):
    service = GetByIdService(SizeController)
    return service.run(_id)


@size.route("/", methods=GET)
def get_sizes():
    service = GetAllService(SizeController)
    return service.run()
