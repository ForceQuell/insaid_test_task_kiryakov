from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
import inject
from settings import Settings
from aiopg.sa import Engine, create_engine
from typing import Optional

from routers.router import router
from repositories import Repository


engine: Optional[Engine] = None


app = FastAPI()
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Get the original 'detail' list of errors
    details = exc.errors()
    if {
        'loc': ('header', 'auth'),
        'msg': 'field required',
        'type': 'value_error.missing'
    } in details:
        return JSONResponse(
            status_code=401,
            content=jsonable_encoder("auth token required!")
        )
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": details}),
    )


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
