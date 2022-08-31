from typing import Optional
from repositories import Repository
from utils import auth, exceptions
import inject

from models import (
    RegisterDataModel,
    User,
    AuthDataModel,
    TokenAnswerModel,
)


SERVICE: Optional['Service'] = None


def get_service() -> 'Service':
    global SERVICE
    if SERVICE is None:
        SERVICE = Service()
    return SERVICE


@inject.autoparams()
class Service:
    def __init__(
        self,
        repository: Repository
    ):
        self._repository = repository
    
    async def register_user(self, register_data: RegisterDataModel) -> str:
        user = User(
            name=register_data.name,
            password=auth.get_password_hash(register_data.password),
        )
        result = await self._repository.register_user(user)
        if not result:
            raise exceptions.UserNameAlreadyExists
        return result

    async def auth(self, auth_data: AuthDataModel) -> TokenAnswerModel:
        auth_data.password = auth.get_password_hash(auth_data.password)
        result_user = await self._repository.check_user(auth_data)
        if not result_user:
            raise exceptions.BadCredentials
        return TokenAnswerModel(token=auth.user_to_jwt(result_user))
