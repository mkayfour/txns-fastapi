from datetime import datetime

from pydantic import BaseModel

from enum import Enum


class TransactionTypesEnum(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class TransactionBase(BaseModel):
    transaction_type: TransactionTypesEnum
    amount: int
    timestamp: datetime
    user_id: int


class User(BaseModel):
    id: int
    firstname: str
    email: str

    class Config:
        orm_mode = True


class TransactionDisplay(BaseModel):
    id: int
    transaction_type: TransactionTypesEnum
    amount: int
    timestamp: datetime
    user: User

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
