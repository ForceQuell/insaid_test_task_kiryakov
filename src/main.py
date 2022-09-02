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


# движок подключения к БД
engine: Optional[Engine] = None


# инстанс приложения
app = FastAPI()

# добавляем роутер
app.include_router(router)


# переопределение стандартной ошибки валидации, чтобы отдавать 401 если не передан jwt-токен
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


# конфиг соответствий тип -> объект
# Работает следующим образом:
#   Если использовать декоратор @inject.autoparams() над методом или классом
#   то при использовании (вызове метода/создания экземпляра класса) inject
#   автоматически подставит нужный объект в аргументы в зависимости от типа.
def config(binder):
    global engine
    repo = Repository(engine)

    # -----------тип----объект
    binder.bind(Engine, engine)
    binder.bind(Repository, repo)


@app.on_event('startup')
async def startup_event():
    # при старте приложения инициализируем движок подключения к БД
    global engine
    engine = await create_engine(
        host=Settings.PG_HOST,
        port=Settings.PG_PORT,
        user=Settings.PG_USER,
        dbname=Settings.PG_DB,
        password=Settings.PG_PASS
    ).__aenter__()

    # "применить конфиг"
    inject.configure(config)


@app.on_event('shutdown')
async def shutdown_event():
    global engine
    await engine.__aexit__(None, None, None)

"""
В целом, идея -- реализовать архитектуру сервиса,
разделенную на 3 слоя:
    роутер -> логика -> инфраструктура(методы взаимодействия с БД или иными источниками),
которую можно будет легко масштабировать и тестировать.
"""
