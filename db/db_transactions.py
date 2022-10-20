from datetime import datetime

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm.session import Session

from db.models import DbTransaction, DbUser
from db.schemas import TransactionBase, UserDisplay


def get_transactions(db: Session, current_user):
    user = db.query(DbUser).filter(DbUser.email == current_user.email).first()
    return db.query(DbTransaction).filter(DbTransaction.user_id == user.id).all()


def create_transaction(db: Session, request: TransactionBase, current_user:UserDisplay):
    user = db.query(DbUser).filter(DbUser.email == current_user.email).first()
    new_txn = DbTransaction(
        transaction_type=request.transaction_type,
        amount=request.amount,
        timestamp=datetime.now(),
        user_id=user.id,
    )

    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return new_txn


def delete_transaction(db: Session, txn_id: int, current_user: UserDisplay):
    transaction = (
        db.query(DbTransaction).filter(DbTransaction.id == txn_id).first()
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with {txn_id} not found",
        )

    # user = db.query(DbUser).filter(DbUser.email == transaction.user.email).first()

    if transaction.user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This does not belong to you")

    db.delete(transaction)
    db.commit()
    return "ok"
