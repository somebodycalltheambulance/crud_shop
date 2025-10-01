import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app")


class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except ValueError as e:  # наши бизнес-ошибки
            return JSONResponse({"detail": str(e)}, status_code=400)
        except Exception:  # всё остальное
            logger.exception("Unhandled error")
            return JSONResponse({"detail": "Internal Server Error"}, status_code=500)
