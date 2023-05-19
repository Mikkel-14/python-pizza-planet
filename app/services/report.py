from app.common.http_methods import GET
from flask import Blueprint

from ..controllers import ReportController
from .service_template import GetAllService

report = Blueprint("report", __name__)


@report.route("/", methods=GET)
def get_report():
    service = GetAllService(ReportController)
    return service.run()
