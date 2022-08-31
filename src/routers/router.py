from fastapi import APIRouter, Depends, HTTPException
from services import Service, get_service
from models import (
    RegisterDataModel,
    AuthDataModel,
    TokenAnswerModel,
    MessageModel,
)


router = APIRouter()


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


@router.post("/send_message")
async def post_send(
    mesage: MessageModel
):
    pass
