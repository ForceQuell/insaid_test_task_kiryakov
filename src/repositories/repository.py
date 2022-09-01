from os import access
from typing import Optional
from uuid import UUID
import inject
from aiopg.sa import Engine
from sqlalchemy import select, desc, and_
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from utils import exceptions

from .db_models import (
    users,
    messages
)

from models import (
    User,
    AuthDataModel,
    MessageModel,
    MessageModelInner
)


REPOSITORY: Optional['Repository'] = None

def get_repository() -> 'Repository':
    global REPOSITORY
    if REPOSITORY is None:
        REPOSITORY = Repository()
    return REPOSITORY

class Repository:
    @inject.autoparams()
    def __init__(self, engine: Engine):
        self._db = engine

    async def register_user(self, user: User) -> Optional[str]:
        query = users.insert().values([user.dict()])
        async with self._db.acquire() as conn:
            try:
                await conn.execute(query)
            except UniqueViolation:
                return None
            return user.name

    async def check_user(self, auth_data: AuthDataModel) -> Optional[User]:
        query = select(
            [
                users
            ]
        ).where(
            and_(
                users.c.name == auth_data.name,
                users.c.password == auth_data.password
            )   
        )
        async with self._db.acquire() as conn:
            result = await conn.execute(query)
            return User.from_row(**(await result.fetchone())) if result.rowcount else None

    async def get_user_by_name(self, name: str) -> Optional[User]:
        query = select(
            [
                users
            ]
        ).where(users.c.name == name)
        async with self._db.acquire() as conn:
            result = await conn.execute(query)
            return User.from_row(**(await result.fetchone())) if result.rowcount else None

    async def post_message(self, message: MessageModelInner) -> bool:
        query = messages.insert().values([message.__dict__])
        async with self._db.acquire() as conn:
            try:
                await conn.execute(query)
            except ForeignKeyViolation:
                return False
        return True

    async def get_last_messages(self, count: int) -> list[MessageModel]:
        query = select(
            [
                messages.c.name,
                messages.c.message
            ]
        ).limit(count).order_by(desc(messages.c.timestamp))

        async with self._db.acquire() as conn:
            result = await conn.execute(query)
            return [MessageModel(**row) for row in (await result.fetchall())]
