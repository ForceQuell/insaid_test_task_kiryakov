from typing import Optional, Union
from uuid import uuid4
from datetime import datetime
from repositories import Repository
from utils import auth, exceptions
import inject

from re import compile, match


from models import (
    RegisterDataModel,
    User,
    AuthDataModel,
    TokenAnswerModel,
    MessageModel,
    MessageModelInner,
    User,
)


history_command_pattern = compile(r'^history\ \d+')


# сиглтон объекта сервиса (под сервисом тут имеется в виду слой логики)
SERVICE: Optional['Service'] = None


def get_service() -> 'Service':
    global SERVICE
    if SERVICE is None:
        SERVICE = Service()
    return SERVICE


class Service:
    @inject.autoparams()
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

    async def send_message_parse(self, message: MessageModel) -> Union[list[MessageModel], bool]:
        if match(history_command_pattern, message.message):
            return await self._repository.get_last_messages(message.message.split(' ')[1])
        else:
            message_inner = MessageModelInner(
                id = uuid4(),
                name=message.name,
                message=message.message,
                timestamp=datetime.now()
            )
            if not (await self._repository.post_message(message=message_inner)):
                raise exceptions.NonExistentSenderName
            return True
