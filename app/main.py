from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_user import router as user_router
from app.api.v1.routes_auth import router as auth_router
from app.core.logger import logger
from app.core.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 FastAPI application starting...")
    yield
    logger.info("🛑 FastAPI application shutting down...")

app = FastAPI(lifespan=lifespan)


app.add_middleware(SecurityHeadersMiddleware)

app.include_router(health_router, prefix="/api/v1", tags=["Health"])
app.include_router(user_router, prefix="/api/v1", tags=["User"])
app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Auth Service",
        version="1.0.0",
        description="JWT-secured API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def root():
    return {"message": "Auth Service is up"}
