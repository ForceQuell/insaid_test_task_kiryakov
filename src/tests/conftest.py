import asyncio
import pytest
import pytest_asyncio
from uuid import uuid4
from aiopg.sa import create_engine, Engine
from sqlalchemy import create_engine as create_sync_engine
from repositories.db_models import metadata, users, messages
from main import app, startup_event, shutdown_event
from fastapi.testclient import TestClient
from httpx import AsyncClient
from settings import Settings

from datetime import datetime, timedelta
from utils import auth
import utils_for_test as ut

from repositories import Repository
from services import Service
from models import (
    User,
    MessageModel,
    MessageModelInner,
)


# event loop, нужен для создания асинхронного окружения движка БД 
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# фикстура, возвращающая объект подключения к БД
@pytest_asyncio.fixture(scope="session")
async def test_db(event_loop) -> Engine:
    Settings.PG_DB = Settings.TEST_DB
    async with create_engine(
        user=Settings.PG_USER,
        password=Settings.PG_PASS,
        host=Settings.PG_HOST,
        port=Settings.PG_PORT,
        dbname=Settings.PG_DB,
    ) as test_engine:
        sync_engine = create_sync_engine(Settings.get_db_sync_url())
        with sync_engine.begin() as sync_conn:
            metadata.drop_all(sync_conn)
            metadata.create_all(sync_conn)
        yield test_engine
        with sync_engine.begin() as sync_conn:
            metadata.drop_all(sync_conn)


# инициализация приложения, нужно для тестирования роутов
@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_app():
    Settings.PG_DB = Settings.TEST_DB
    await startup_event()
    yield
    await shutdown_event()


# фикстура, возвращающая объект приложения
@pytest_asyncio.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as async_client:
        yield async_client


# фикстура репозитория
@pytest.fixture
def repository(test_db: Engine) -> Repository:
    return Repository(test_db)


# фикстура сервиса
@pytest.fixture
def service(repository: Repository) -> Service:
    return Service(repository)


# ----- различные фикстуры для создания необходимых условий тестирования -----

@pytest.fixture
def sample_user() -> User:
    return User(
        name=ut.generate_random_string(),
        password=ut.generate_random_string()
    )


@pytest.fixture
def sample_users() -> list[User]:
    return [
        User(
            name=ut.generate_random_string(),
            nickname=ut.generate_random_string(),
            email=ut.generate_random_string(),
            password=ut.generate_random_string()
        ) for _ in range(100)
    ]


@pytest_asyncio.fixture
async def inserted_user(
    sample_user: User,
    test_db: Engine
) -> User:
    async with test_db.acquire() as conn:
        await conn.execute(
            users.insert().values(
                [
                    sample_user.dict()
                ]
            )
        )
    yield sample_user
    async with test_db.acquire() as conn:
        async with conn.begin():
            await conn.execute(messages.delete())
            await conn.execute(users.delete())


@pytest_asyncio.fixture
async def inserted_users(
    sample_users: list[User],
    test_db: Engine
) -> list[User]:
    async with test_db.acquire() as conn:
        await conn.execute(
            users.insert().values(
                [
                    user.dict() for user in sample_users
                ]
            )
        )
    yield sample_users
    async with test_db.acquire() as conn:
        async with conn.begin():
            await conn.execute(messages.delete())
            await conn.execute(users.delete())


@pytest_asyncio.fixture
async def registered_user(
    sample_user: User,
    test_db: Engine
) -> User:
    encoded_model = User(
        id=sample_user.id,
        name=sample_user.name,
        password=auth.get_password_hash(sample_user.password)
    )
    async with test_db.acquire() as conn:
        await conn.execute(
            users.insert().values(
                [
                    encoded_model.dict()
                ]
            )
        )
    yield sample_user
    async with test_db.acquire() as conn:
        async with conn.begin():
            await conn.execute(messages.delete())
            await conn.execute(users.delete())


@pytest.fixture
def inserted_user_token(inserted_user: User) -> tuple[User, str]:
    return inserted_user, auth.user_to_jwt(inserted_user)


@pytest.fixture
def sample_messages(inserted_users: list[User]) -> list[MessageModel]:
    return [
        MessageModel(
            name=user.name,
            message=ut.generate_random_string()
        )
        for user in inserted_users
    ]

@pytest.fixture
def sample_messages_inner(sample_messages: list[MessageModel]) -> list[MessageModelInner]:
    return [
        MessageModelInner(
            name=message.name,
            message=message.message,
            id=uuid4(),
            timestamp=datetime.now() + timedelta(seconds=time_shift)
        )
        for message, time_shift in zip(sample_messages, range(len(sample_messages)))
    ]


@pytest_asyncio.fixture
async def inserted_messages(
    sample_messages_inner: list[MessageModelInner],
    test_db: Engine
) -> list[MessageModelInner]:
    async with test_db.acquire() as conn:
        await conn.execute(
            messages.insert().values(
                [
                    message.__dict__ for message in sample_messages_inner
                ]
            )
        )
    yield sample_messages_inner
    async with test_db.acquire() as conn:
        async with conn.begin():
            await conn.execute(messages.delete())
            await conn.execute(users.delete())
