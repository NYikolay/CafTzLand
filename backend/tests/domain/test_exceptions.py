from domain.exceptions import ConflictError, DomainError, NotFoundError, ValidationError


def test_domain_error_defaults() -> None:
    error = DomainError()
    assert error.code == "domain_error"
    assert error.status_code == 400
    assert str(error) == "domain_error"


def test_not_found_error() -> None:
    error = NotFoundError("Task not found")
    assert error.code == "not_found"
    assert error.status_code == 404
    assert str(error) == "Task not found"


def test_conflict_error() -> None:
    error = ConflictError("Already exists")
    assert error.code == "conflict"
    assert error.status_code == 409


def test_validation_error() -> None:
    error = ValidationError("Выбранный кофе больше недоступен")
    assert error.code == "validation_error"
    assert error.status_code == 422
    assert str(error) == "Выбранный кофе больше недоступен"
