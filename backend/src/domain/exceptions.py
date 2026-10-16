class DomainError(Exception):
    code: str = "domain_error"
    status_code: int = 400

    def __init__(self, message: str = "") -> None:
        self.message = message or self.code
        super().__init__(self.message)


class NotFoundError(DomainError):
    code = "not_found"
    status_code = 404


class ConflictError(DomainError):
    code = "conflict"
    status_code = 409


class ValidationError(DomainError):
    code = "validation_error"
    status_code = 422
