from fastapi import HTTPException, status


class BaseCustomException(HTTPException):
    """Base exception class for custom exceptions."""
    pass


class AuthenticationError(BaseCustomException):
    """Authentication related errors."""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class AuthorizationError(BaseCustomException):
    """Authorization related errors."""
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotFoundError(BaseCustomException):
    """Resource not found errors."""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ValidationError(BaseCustomException):
    """Validation related errors."""
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class ConflictError(BaseCustomException):
    """Conflict related errors."""
    def __init__(self, detail: str = "Resource conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)