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
    # тест добавления в базу нового пользователя
    result = await repository.register_user(sample_user)
    assert result == sample_user.name

    # тест попытки добавления в базу существующего пользователя
    sample_user.id = uuid4()
    assert (await repository.register_user(sample_user)) is None


@pytest.mark.asyncio
async def test_check_user(inserted_user: User, repository: Repository):
    # тест проверки пользователя
    auth_data = AuthDataModel(
        name=inserted_user.name,
        password=inserted_user.password
    )
    assert (await repository.check_user(auth_data)) == inserted_user

    # тест проверки несуществующего пользователя
    auth_data.name = auth_data.name + '.'
    assert (await repository.check_user(auth_data)) == None


@pytest.mark.asyncio
async def test_get_user_by_name(inserted_users: User, repository: Repository):
    # тест получения пользователя по имени
    random_user = random.choice(inserted_users)
    assert (await repository.get_user_by_name(random_user.name)) == random_user

    # тест получения несуществующего пользователя по имени
    assert (await repository.get_user_by_name(random_user.name + '.')) == None


@pytest.mark.asyncio
async def test_post_message(sample_messages_inner: list[MessageModelInner], repository: Repository):
    random_message = random.choice(sample_messages_inner)
    
    # тест добавления сообщения в базу
    assert (await repository.post_message(random_message)) == True

    # тест добавления сообщения в базу от имени несуществующего пользователя
    random_message.id = uuid4()
    random_message.name += '.'
    assert (await repository.post_message(random_message)) == False


@pytest.mark.asyncio
async def test_get_last_messages(inserted_messages: list[MessageModelInner], repository: Repository):
    # тест получения последних n сообщений из базы
    n = 25
    expected = [
        MessageModel(
            name=message.name,
            message=message.message
        )
        for message in sorted(inserted_messages, key=lambda x: x.timestamp, reverse=True)[:n]
    ]
    assert (await repository.get_last_messages(n)) == expected
