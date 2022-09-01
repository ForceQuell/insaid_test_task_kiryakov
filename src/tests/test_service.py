import pytest
import random

from utils import exceptions, auth
from services import Service

from models import (
    User,
    RegisterDataModel,
    AuthDataModel,
    TokenAnswerModel,
    MessageModel,
    MessageModelInner,
)


@pytest.mark.asyncio
async def test_register_user(inserted_users: list[User], service: Service):
    random_user = random.choice(inserted_users)
    register_data = RegisterDataModel(
        name=random_user.name,
        password=random_user.password
    )
    with pytest.raises(exceptions.UserNameAlreadyExists):
        await service.register_user(register_data)
    register_data.name += '.'
    assert (await service.register_user(register_data)) == register_data.name


@pytest.mark.asyncio
async def test_auth(registered_user: User, service: Service):
    auth_data = AuthDataModel(
        name=registered_user.name,
        password=registered_user.password
    )
    assert (await service.auth(auth_data)) == TokenAnswerModel(token=auth.user_to_jwt(registered_user))

    auth_data.password += '.'
    with pytest.raises(exceptions.BadCredentials):
        await service.auth(auth_data)


@pytest.mark.asyncio
async def test_send_message_parse(sample_messages: list[MessageModel], inserted_messages: list[MessageModelInner], service: Service):
    random_message = random.choice(sample_messages)

    n = 25
    get_history_message = MessageModel(
        name=random_message.name,
        message=f'history {n}'
    )

    assert (
        await service.send_message_parse(get_history_message)
    ) == [
        MessageModel(
            name=message.name,
            message=message.message
        )
        for message in sorted(inserted_messages, key=lambda x: x.timestamp, reverse=True)[:n]
    ]
 
    assert (await service.send_message_parse(random_message)) == True

    with pytest.raises(exceptions.NonExistentSenderName):
        random_message.name += '.'
        await service.send_message_parse(random_message)
