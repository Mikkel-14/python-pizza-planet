from abc import ABC, abstractclassmethod
from typing import Optional, Any, Tuple

from flask import jsonify

from ..controllers import BaseController


class ServiceTemplate(ABC):
    def __init__(self, controller: BaseController):
        self.controller = controller

    def run(self, request_data: Optional[Any] = None):
        entity, error = self.make_request(request_data)
        return self.parse_and_return_response(entity, error)

    @abstractclassmethod
    def make_request(self, request_data: Optional[Any]) -> Tuple[Any, Optional[str]]:
        raise NotImplementedError("Not implemented")

    def parse_and_return_response(self, entity, error):
        response = entity if not error else {"error": error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code


class GetAllService(ServiceTemplate):
    def make_request(self, request_data: Optional[Any]) -> Tuple[Any, Optional[str]]:
        return self.controller.get_all()


class CreateService(ServiceTemplate):
    def make_request(self, request_data: Optional[Any]) -> Tuple[Any, Optional[str]]:
        return self.controller.create(request_data)


class UpdateService(ServiceTemplate):
    def make_request(self, request_data: Optional[Any]) -> Tuple[Any, Optional[str]]:
        return self.controller.update(request_data)


class GetByIdService(ServiceTemplate):
    def make_request(self, request_data: Optional[Any]) -> Tuple[Any, Optional[str]]:
        return self.controller.get_by_id(request_data)
