from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import IngredientController
from .service_template import CreateService, UpdateService, GetByIdService, GetAllService

ingredient = Blueprint("ingredient", __name__)


@ingredient.route("/", methods=POST)
def create_ingredient():
    service = CreateService(IngredientController)
    return service.run(request.json)


@ingredient.route("/", methods=PUT)
def update_ingredient():
    service = UpdateService(IngredientController)
    return service.run(request.json)


@ingredient.route("/id/<_id>", methods=GET)
def get_ingredient_by_id(_id: int):
    service = GetByIdService(IngredientController)
    return service.run(_id)


@ingredient.route("/", methods=GET)
def get_ingredients():
    service = GetAllService(IngredientController)
    return service.run()
