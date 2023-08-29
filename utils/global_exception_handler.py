from fastapi.encoders import jsonable_encoder
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.exceptions import HTTPException
from dto.exceptions.not_found_exception import NotFoundException
from dto.exceptions.bad_request_exception import BadRequestException


class GlobalExceptionHandler:
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        return JSONResponse(status_code=exc.status_code,
                            content=jsonable_encoder({"code": exc.status_code, "message": exc.message}))
    async def bad_request_exception_handler(request: Request, exc: BadRequestException):
        return JSONResponse(status_code=exc.status_code,
                            content=jsonable_encoder({"code": exc.status_code, "message": exc.message}))
    async def internal_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(status_code=500,
                            content=jsonable_encoder({"code": 500, "message": "Internal Server Error"}))


