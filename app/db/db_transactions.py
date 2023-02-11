# import calendar
from datetime import datetime

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm.session import Session
from sqlalchemy import desc, extract
from db.models import DbTransaction, DbUser
from db.schemas import TransactionBase, TransactionTypesEnum, UserDisplay
from fastapi.responses import JSONResponse


def get_transactions(db: Session, current_user):
    # currentMonth = datetime.now().month
    # currentYear = datetime.now().year
    user = db.query(DbUser).filter(DbUser.email == current_user.email).first()

    return (
        db.query(DbTransaction)
        .filter(DbTransaction.user_id == user.id)
        # .filter(extract("year", DbTransaction.timestamp) == 2023)
        .order_by(desc(DbTransaction.timestamp))
        .all()
    )


def create_transaction(
    db: Session, request: TransactionBase, current_user: UserDisplay
):
    user = db.query(DbUser).filter(DbUser.email == current_user.email).first()
    new_txn = DbTransaction(
        transaction_type=request.transaction_type,
        name=request.name,
        amount=request.amount,
        timestamp=datetime.now(),
        user_id=user.id,
    )

    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return new_txn


def edit_transaction(
    db: Session,
    request: TransactionBase,
    transaction_id: int,
    current_user: UserDisplay,
):
    user = db.query(DbUser).filter(DbUser.email == current_user.email).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    transaction: TransactionBase = (
        db.query(DbTransaction)
        .filter(
            DbTransaction.id == transaction_id and DbTransaction.user == user
        )
        .first()
    )

    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    transaction_data = request.dict(exclude_unset=True)

    for key, value in transaction_data.items():
        setattr(transaction, key, value)

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This does not belong to you",
        )

    db.delete(transaction)
    db.commit()
    return "ok"


def get_total_amount(db: Session, current_user: UserDisplay):
    transactions = (
        db.query(DbTransaction)
        .filter(DbTransaction.user == current_user)
        .all()
    )

    total_debit_amount = 0
    total_credit_amount = 0

    debit_txns = 0
    credit_txns = 0

    for values in transactions:
        if values.transaction_type == TransactionTypesEnum.CREDIT:
            total_credit_amount += values.amount
            credit_txns += 1
        if values.transaction_type == TransactionTypesEnum.DEBIT:
            total_debit_amount += values.amount
            debit_txns += 1

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "total_amount": {
                "credit": total_credit_amount,
                "debit": total_debit_amount,
            },
            "transactions_count": {"credit": credit_txns, "debit": debit_txns},
        },
    )
