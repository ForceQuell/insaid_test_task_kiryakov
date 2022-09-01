import pytest
import random
from uuid import uuid4

from repositories import Repository
from models import (
    User,
    AuthDataModel,
    MessageModel,
    MessageModelInner,
)


@pytest.mark.asyncio
async def test_register_user(sample_user: User, repository: Repository):
    expected = sample_user.name
    result = await repository.register_user(sample_user)
    assert result == expected
    sample_user.id = uuid4()
    assert (await repository.register_user(sample_user)) is None


@pytest.mark.asyncio
async def test_check_user(inserted_user: User, repository: Repository):
    auth_data = AuthDataModel(
        name=inserted_user.name,
        password=inserted_user.password
    )
    assert (await repository.check_user(auth_data)) == inserted_user

    auth_data.name = auth_data.name + '.'
    assert (await repository.check_user(auth_data)) == None

    auth_data.name = inserted_user.name
    auth_data.password = auth_data.password + '.'
    assert (await repository.check_user(auth_data)) == None

    auth_data.name = inserted_user.name + '.'
    assert (await repository.check_user(auth_data)) == None


@pytest.mark.asyncio
async def test_get_user_by_name(inserted_users: User, repository: Repository):
    random_user = random.choice(inserted_users)
    assert (await repository.get_user_by_name(random_user.name)) == random_user
    assert (await repository.get_user_by_name(random_user.name + '.')) == None


@pytest.mark.asyncio
async def test_post_message(sample_messages_inner: list[MessageModelInner], repository: Repository):
    random_message = random.choice(sample_messages_inner)
    assert (await repository.post_message(random_message)) == True
    random_message.id = uuid4()
    random_message.name += '.'
    assert (await repository.post_message(random_message)) == False


@pytest.mark.asyncio
async def test_get_last_messages(inserted_messages: list[MessageModelInner], repository: Repository):
    n = 25
    expected = [
        MessageModel(
            name=message.name,
            message=message.message
        )
        for message in sorted(inserted_messages, key=lambda x: x.timestamp, reverse=True)[:n]
    ]
    assert (await repository.get_last_messages(n)) == expected
