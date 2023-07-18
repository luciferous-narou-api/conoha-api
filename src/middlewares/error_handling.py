from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from src.utils.my_logger import MyLogger

logger = MyLogger(__name__)

class MiddlewareErrorHandling(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"error occurred: [{type(e)}] {e}")
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message": "Internal Server Error",
                },
            )
