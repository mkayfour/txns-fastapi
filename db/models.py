from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Enum
import enum
from sqlalchemy.orm import relationship
from .database import Base


class TransactionTypes(str, enum.Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class DbUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    password = Column(String)
    transactions = relationship("DbTransaction", back_populates="user")
    tags = relationship("DbTag", back_populates="user")


class DbTransaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(
        Enum(TransactionTypes), nullable=False, default=TransactionTypes.DEBIT
    )
    amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("DbUser", back_populates="transactions")


class DbTag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("DbUser", back_populates="tags")
