from fastapi import APIRouter, Depends
from typing import Union
from services import Service, get_service
from utils import auth
from models import (
    RegisterDataModel,
    AuthDataModel,
    TokenAnswerModel,
    MessageModel,
    User,
)


router = APIRouter()


"""
Механизм Depends в fastapi вызывает указанный метод
и расширяет требования эндпоинта на набор аргументов, указанных в этом методе
"""


@router.post("/register")
async def post_register(
    register_data: RegisterDataModel,
    service: Service = Depends(get_service)
) -> str:
    return await service.register_user(register_data)


@router.post("/auth", response_model=TokenAnswerModel)
async def post_auth(
    auth_data: AuthDataModel,
    service: Service = Depends(get_service)
):
    return await service.auth(auth_data)


@router.post("/send_message", response_model=Union[list[MessageModel], bool])
async def post_send(
    message: MessageModel,
    service: Service = Depends(get_service),
    _: User = Depends(auth.auth_user)
):
    return await service.send_message_parse(message)
