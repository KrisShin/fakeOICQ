from fastapi import HTTPException, status

CredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


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


class AuthenticationFailed(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ''

    def __init__(self, detail):
        self.detail = [{'msg': detail}]
