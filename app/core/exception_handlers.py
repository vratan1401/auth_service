from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.logger import logger

def format_error_response(error_type: str, message: str, status_code: int):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "type": error_type,
                "message": message,
                "status_code": status_code,
            }
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException: {exc.detail} [{exc.status_code}]")
    return format_error_response("HTTPException", exc.detail, exc.status_code)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc}")
    return format_error_response("RequestValidationError", str(exc), 422)

async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception occurred")
    return format_error_response("InternalServerError", "An unexpected error occurred.", 500)
