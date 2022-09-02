from dataclasses import dataclass
from dotenv import load_dotenv
from os import environ


if not environ.get("IGNORE_DOTENV"):
    load_dotenv()


class Settings:
    PG_HOST: str = environ.get('PG_HOST')
    PG_PORT: str = environ.get('PG_PORT')
    PG_USER: str = environ.get('PG_USER')
    PG_DB: str = environ.get('PG_DB')
    PG_PASS: str = environ.get('PG_PASS')
    TEST_DB: str = environ.get('TEST_DB', default='test_db')

    JWT_SECRET_KEY: str = environ.get('JWT_SECRET_KEY')
    JWT_ALGORITHM: str = 'HS256'

    @classmethod
    def get_db_sync_url(cls) -> str:
        return f'postgresql://{cls.PG_USER}:{cls.PG_PASS}@{cls.PG_HOST}:{cls.PG_PORT}/{cls.PG_DB}'
