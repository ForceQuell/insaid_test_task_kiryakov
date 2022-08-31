import jwt
from settings import Settings
from models import User, TokenPayload
from hashlib import sha256


def user_to_jwt(user: User) -> str:
    return jwt.encode(payload={"name": user.name}, key=Settings.JWT_SECRET_KEY)


def get_password_hash(password: str) -> str:
    return sha256(bytes(password, 'utf-8')).hexdigest()
