from datetime import datetime

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm.session import Session

from db.models import DbTransaction
from db.schemas import TransactionBase


def get_transactions(db: Session):
    return db.query(DbTransaction).all()


def create_transaction(db: Session, request: TransactionBase):
    new_txn = DbTransaction(
        transaction_type=request.transaction_type,
        amount=request.amount,
        timestamp=datetime.now(),
        user_id=1,  # request.creator_id,
    )

    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return new_txn


def delete_transaction(db: Session, id: int):
    transaction = (
        db.query(DbTransaction).filter(DbTransaction.id == id).first()
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with {id} not found",
        )

    db.delete(transaction)
    db.commit()
    return "ok"
