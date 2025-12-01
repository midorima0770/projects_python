from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status
import logging

from starlette.responses import Response

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Базовый класс всех кастомных ошибок."""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

# Универсальный обработчик ошибок для FastAPI
async def app_exception_handler(request: Request, exc: AppException) -> Response:
    logger.warning(f"Handled exception: {exc.__class__.__name__} - {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "path": str(request.url)
        },
    )
