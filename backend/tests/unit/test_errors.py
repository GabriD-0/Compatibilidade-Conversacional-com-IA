import pytest
from app.errors import ApiError


@pytest.mark.unit
def test_api_error_exposes_payload_fields():
    error = ApiError(
        "Mensagem",
        status_code=422,
        code="invalid_payload",
        details={"field": "email"},
    )

    assert str(error) == "Mensagem"
    assert error.message == "Mensagem"
    assert error.status_code == 422
    assert error.code == "invalid_payload"
    assert error.details == {"field": "email"}
