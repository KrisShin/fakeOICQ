from fastapi import HTTPException, status


class BadRequest(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ''

    def __init__(self, detail):
        self.detail = [{'msg': detail}]


class NotFound(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = ''

    def __init__(self, detail):
        self.detail = [{'msg': detail}]


class TooManyRequest(HTTPException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    detail = ''

    def __init__(self, detail):
        self.detail = [{'msg': detail}]


class AuthorizationFailed(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ""
    headers = {"WWW-Authenticate": "Bearer"}

    def __init__(self, detail="Could not validate credentials"):
        self.detail = [{'msg': detail}]
