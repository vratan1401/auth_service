from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        response.headers["X-Frame-Options"] = "DENY"

        response.headers["X-Content-Type-Options"] = "nosniff"

        response.headers["X-XSS-Protection"] = "1; mode=block"

        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"

        return response
