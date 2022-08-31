from fastapi import Depends, Header
import jwt
from settings import Settings
from models import User, TokenPayload
from hashlib import sha256
from utils import exceptions
from repositories import Repository, get_repository


def user_to_jwt(user: User) -> str:
    return jwt.encode(
        payload={"name": user.name},
        key=Settings.JWT_SECRET_KEY,
        algorithm=Settings.JWT_ALGORITHM
    )


def get_password_hash(password: str) -> str:
    return sha256(bytes(password, 'utf-8')).hexdigest()


def auth_user(
    auth: str = Header(regex="Bearer_([a-zA-Z0-9_=]+)\.([a-zA-Z0-9_=]+)\.([a-zA-Z0-9_\-\+\/=]*)"),
    repository: Repository = Depends(get_repository)
) -> User:
    token = auth[7:]
    payload = jwt.decode(
        token,
        Settings.JWT_SECRET_KEY,
        algorithms=[Settings.JWT_ALGORITHM]
    )
    user = repository.get_user_by_name(payload["name"])
    if not user:
        raise exceptions.BadAuthToken
    return user
