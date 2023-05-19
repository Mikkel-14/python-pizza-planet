import pytest


def test_get_report_service(client, report_uri, create_orders):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith("200"))
    returned_report = response.json
    pytest.assume(returned_report["ingredient"])
    pytest.assume(returned_report["month"])
    pytest.assume(returned_report["revenue"])
    pytest.assume(returned_report["clients"])
