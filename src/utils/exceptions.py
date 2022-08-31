from fastapi import HTTPException


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
