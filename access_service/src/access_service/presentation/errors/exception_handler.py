from fastapi import Request, Response
from fastapi.responses import JSONResponse

from access_service.domain.common.exceptions.base import BaseError
from access_service.presentation.errors.http_errors import ErrorEnum, HTTP_ERRORS, ErrorInfo


def get_error(error: BaseError):
    error_name = ErrorEnum[type(error)]
    error_info: ErrorInfo = HTTP_ERRORS.get_http_error(error_name)
    return JSONResponse(
        status_code=error_info.status_code,
        content={"error": error_info.content.error_code, "message": error_info.content.message},
    )

def app_exception_handler(request: Request, exc: Exception) -> Response:
    if not isinstance(exc, BaseError):
        return JSONResponse(status_code=500, content={})
    
    return get_error(exc)