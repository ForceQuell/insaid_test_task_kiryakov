import pytest
import random
from httpx import AsyncClient
from utils import auth

from models import (
    User,
    MessageModelInner,
    MessageModel,
)


@pytest.mark.asyncio
async def test_post_register(sample_user: User, inserted_users: list[User], async_client: AsyncClient):
    # тест регистрации пользователя
    response = await async_client.post(
        url="/register",
        json=sample_user.dict(exclude={"id"})
    )
    assert response.json() == sample_user.name

    # тест ошибки, если пользователь с переданным именем уже зарегистрирован
    response = await async_client.post(
        url="/register",
        json=sample_user.dict(exclude={"id"})
    )
    assert response.json() == {'detail': 'Such name already exists'}


@pytest.mark.asyncio
async def test_post_auth(registered_user: User, async_client: AsyncClient):
    # тест возврата jwt-токена
    response = await async_client.post(
        url='/auth',
        json={
            "name": registered_user.name,
            "password": registered_user.password
        }
    )
    assert response.json() == {'token': auth.user_to_jwt(registered_user)}

    # тест ошибки, если переданы неверные креды
    response = await async_client.post(
        url='/auth',
        json={
            "name": registered_user.name,
            "password": registered_user.password + '.'
        }
    )
    assert response.json() == {'detail': 'Username or password incorrect'}


@pytest.mark.asyncio
async def test_post_send(
    inserted_user_token: tuple[User, str],
    inserted_messages: list[MessageModelInner],
    async_client: AsyncClient
):
    user = inserted_user_token[0]
    jwt_token = inserted_user_token[1]

    # тест ошибки, если jwt-токен не передается
    response = await async_client.post(
        url='/send_message',
        json={
            "name": user.name,
            "message": "test_message"
        }
    )
    assert response.json() == 'auth token required!' and response.status_code == 401

    # тест ошибки, если jwt передан в неверном формате
    response = await async_client.post(
        url='/send_message',
        json={
            "name": user.name,
            "message": "test_message"
        },
        headers={
            "auth": f"{jwt_token}"
        }
    )
    assert response.status_code == 422

    # тест полученя последних n сообщений
    n = 25
    response = await async_client.post(
        url='/send_message',
        json={
            "name": user.name,
            "message": f"history {n}"
        },
        headers={
            "auth": f"Bearer_{jwt_token}"
        }
    )
    assert response.json() == [
        MessageModel(
            name=message.name,
            message=message.message
        )
        for message in sorted(
            inserted_messages, key=lambda x: x.timestamp, reverse=True
        )[:n]
    ]

    # тест отправки сообщения
    response = await async_client.post(
        url='/send_message',
        json={
            "name": user.name,
            "message": "test_message"
        },
        headers={
            "auth": f"Bearer_{jwt_token}"
        }
    )
    assert response.json() == True
