from curses.ascii import HT
from fastapi import HTTPException


# сборник кастомных http-ошибок

class UserNameAlreadyExists(HTTPException):
    def __init__(self, message='Such name already exists', status_code=400) -> None:
        super().__init__(
            status_code=status_code,
            detail=message
        )

class BadCredentials(HTTPException):
    def __init__(self, message="Username or password incorrect", status_code=401) -> None:
        super().__init__(
            status_code=status_code,
            detail=message
        )

class BadAuthToken(HTTPException):
    def __init__(self, message="Bad auth token", status_code=401) -> None:
        super().__init__(
            status_code=status_code,
            detail=message
        )


class NonExistentSenderName(HTTPException):
    def __init__(self, message="Such sender name does not exist", status_code=400) -> None:
        super().__init__(
            status_code=status_code,
            detail=message
        )
