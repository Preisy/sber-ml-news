from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, object):
        self.message = f"{object} not found"

    status_code = 404
