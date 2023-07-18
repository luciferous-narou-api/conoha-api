import os
from typing import Optional

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.status import HTTP_401_UNAUTHORIZED


class MiddlewareCheckHeader(BaseHTTPMiddleware):
    api_key: Optional[str] = os.getenv("API_KEY")

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        api_key = request.headers.get("X-API-KEY")
        if api_key == self.api_key:
            return await call_next(request)
        else:
            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content={"message": "Unauthorized"},
            )
