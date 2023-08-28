from fastapi.encoders import jsonable_encoder
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.exceptions import HTTPException


class GlobalExceptionHandler:
    async def internal_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(status_code=500, content=jsonable_encoder({"code": 500, "message": "Internal Server Error"}))
