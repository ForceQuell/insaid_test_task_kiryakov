from curses import meta
from sqlalchemy import Table, Column, MetaData, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, VARCHAR


metadata = MetaData()


users = Table(
    'users',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('name', VARCHAR, unique=True),
    Column('password', VARCHAR)
)

messages = Table(
    'messages',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('name', VARCHAR, ForeignKey('users.name')),
    Column('message', VARCHAR),
    Column('timestamp', DateTime(timezone=True))
)
