from app.domain.exceptions import ConflictError, DomainError, NotFoundError


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
