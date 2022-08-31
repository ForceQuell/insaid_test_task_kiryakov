from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class RegisterDataModel(BaseModel):
    name: str
    password: str


class User(BaseModel):
    name: str
    password: str
    id: Optional[UUID] = Field(default_factory=uuid4)


class AuthDataModel(BaseModel):
    name: str
    password: str


class TokenAnswerModel(BaseModel):
    token: str


class MessageModel(BaseModel):
    name: str
    message: str


class User(BaseModel):
    name: str
    password: str
    id: Optional[UUID] = Field(default_factory=uuid4)

    @classmethod
    def from_row(cls, **kwargs):
        return cls(**kwargs)


class TokenPayload(BaseModel):
    user_id: UUID
    exp: int

    def to_dict(self) -> dict:
        data = self.dict()
        data["user_id"] = str(self.user_id)
        # data["exp"] = str(self.exp)
        return data
