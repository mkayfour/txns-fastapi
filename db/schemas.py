from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from enum import Enum


class User(BaseModel):
    firstname: str
    lastname: Optional[str]
    password: str
    email: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: Optional[str]
    password: str
    username: Optional[str]

    class Config:
        orm_mode = True


class UserDisplay(BaseModel):
    firstname: str
    lastname: str
    email: str

    class Config:
        orm_mode = True


class TransactionTypesEnum(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class TransactionBase(BaseModel):
    transaction_type: TransactionTypesEnum
    amount: int
    timestamp: datetime


class TransactionDisplay(BaseModel):
    id: int
    transaction_type: TransactionTypesEnum
    amount: int
    timestamp: datetime
    user: UserDisplay

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    name: str
    user_id: int

    class Config:
        orm_mode = True


class TagDisplay(BaseModel):
    id: str
    name: str
    user_id: int
    user: User

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
