from fastapi import HTTPException


class BadRequestException(HTTPException):
    def __init__(self):
        self.message = "bad request"

    status_code = 400
