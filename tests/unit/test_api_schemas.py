from src.api.schemas import SOWCreateRequest


def test_sow_create_request_valid():
    data = {"client_id": "C1", "product": "P1", "requirements": "None"}
    model = SOWCreateRequest(**data)
    assert model.client_id == "C1"
    assert model.product == "P1"


def test_sow_create_request_defaults():
    data = {"client_id": "C1", "product": "P1"}
    model = SOWCreateRequest(**data)
    assert model.requirements is None
