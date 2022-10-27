from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm.session import Session

from db.models import DbTransactionTags
from fastapi.responses import JSONResponse


def get_transaction_tags(db: Session, current_user, transaction_id):
    transaction_tags = (
        db.query(DbTransactionTags)
        .filter(DbTransactionTags.transaction_id == transaction_id)
        .all()
    )
    if transaction_tags is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return transaction_tags


def create_transaction_tags(
    db: Session, current_user, transaction_id, tag_ids
):

    for tag_id in tag_ids:
        new_txn_tags = DbTransactionTags(
            transaction_id=transaction_id, tag_id=tag_id
        )
        db.add(new_txn_tags)
        db.commit()
        db.refresh(new_txn_tags)

    return "ok"


def delete_transaction_tags(db: Session, current_user, transaction_tag_id):
    transaction_tag = (
        db.query(DbTransactionTags)
        .filter(DbTransactionTags.id == transaction_tag_id)
        .first()
    )

    if transaction_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    else:
        db.delete(transaction_tag)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Delete successful."},
        )
