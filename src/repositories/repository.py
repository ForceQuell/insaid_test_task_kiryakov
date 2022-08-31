from os import access
from typing import Optional
from uuid import UUID
import inject
from aiopg.sa import Engine
from sqlalchemy import select, insert
from psycopg2.errors import UniqueViolation

from models import (
    User,
    AuthDataModel,
)

from .db_models import (
    users
)

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

    async def check_user(self, auth_data: AuthDataModel) -> User:
        query = select(
            [
                users
            ]
        ).where(
            users.c.name == auth_data.name,
            users.c.password == auth_data.password
        )
        async with self._db.acquire() as conn:
            result = await conn.execute(query)
            result = await result.fetchone()
        return User.from_row(**result)
