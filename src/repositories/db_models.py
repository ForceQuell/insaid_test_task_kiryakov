from sqlalchemy import Table, Column, MetaData
from sqlalchemy.dialects.postgresql import UUID, VARCHAR


metadata = MetaData()


users = Table(
    'users',
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('name', VARCHAR, unique=True),
    Column('password', VARCHAR)
)
