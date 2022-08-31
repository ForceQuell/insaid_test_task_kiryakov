from fastapi import FastAPI
import inject
from settings import Settings
from aiopg.sa import Engine, create_engine
from typing import Optional

from routers.router import router
from repositories import Repository


engine: Optional[Engine] = None


app = FastAPI()
app.include_router(router)


def config(binder):
    global engine
    repo = Repository(engine)
    binder.bind(Engine, engine)
    binder.bind(Repository, repo)


@app.on_event('startup')
async def startup_event():
    global engine
    engine = await create_engine(
        host=Settings.PG_HOST,
        port=Settings.PG_PORT,
        user=Settings.PG_USER,
        dbname=Settings.PG_DB,
        password=Settings.PG_PASS
    ).__aenter__()
    inject.configure(config)


@app.on_event('shutdown')
async def shutdown_event():
    global engine
    await engine.__aexit__(None, None, None)
