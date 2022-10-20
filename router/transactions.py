from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm.session import Session

from db.database import get_db
from db.db_transactions import create_transaction
from db.db_transactions import delete_transaction
from db.db_transactions import get_transactions
from db.db_user import get_current_user
from db.schemas import TransactionBase, UserDisplay
from db.schemas import TransactionDisplay


router = APIRouter(prefix="/transaction", tags=["transactions"])


@router.get("/all", response_model=List[TransactionDisplay])
def posts(
    db: Session = Depends(get_db),
    current_user: UserDisplay = Depends(get_current_user),
):
    return get_transactions(db, current_user)


@router.post("", response_model=TransactionDisplay)
def create(
    request: TransactionBase,
    db: Session = Depends(get_db),
    current_user: UserDisplay = Depends(get_current_user),
):
    return create_transaction(db, request, current_user)


@router.delete("/{id}")
def delete(
    txn_id: int,
    db: Session = Depends(get_db),
    current_user: UserDisplay = Depends(get_current_user),
):
    return delete_transaction(db, txn_id, current_user)

