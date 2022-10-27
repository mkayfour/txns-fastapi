from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm.session import Session

from db.database import get_db
from db.db_transaction_tags import (
    create_transaction_tags,
    delete_transaction_tags,
    get_transaction_tags,
)
from db.db_transactions import create_transaction, get_total_amount
from db.db_transactions import delete_transaction
from db.db_transactions import get_transactions
from db.db_user import get_current_user
from db.schemas import TransactionBase, TransactionTagsDisplay, UserDisplay
from db.schemas import TransactionDisplay


router = APIRouter(prefix="/transaction-tags", tags=["transactions_tags"])


@router.get("/{transaction_id}", response_model=List[TransactionTagsDisplay])
def get(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: UserDisplay = Depends(get_current_user),
):
    return get_transaction_tags(db, current_user, transaction_id)


@router.post(
    "/{transaction_id}",
)
def posts(
    transaction_id: int,
    tag_ids: List[int],
    db: Session = Depends(get_db),
    current_user: UserDisplay = Depends(get_current_user),
):
    return create_transaction_tags(db, current_user, transaction_id, tag_ids)


@router.delete(
    "/{transaction_id}",
)
def delete(
    transaction_tag_id: int,
    db: Session = Depends(get_db),
    current_user: UserDisplay = Depends(get_current_user),
):
    return delete_transaction_tags(db, current_user, transaction_tag_id)
