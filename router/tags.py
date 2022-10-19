from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi import HTTPException, status

from db.database import get_db

from sqlalchemy.orm.session import Session
from db.db_tags import create_tag, delete_tag, get_tags

from db.db_transactions import get_transactions
from db.schemas import TagBase, TagDisplay, TransactionDisplay


router = APIRouter(prefix="/tag", tags=["tags"])


@router.get("/all", response_model=List[TagDisplay])
def tags(
    db: Session = Depends(get_db),
    # current_user: UserAuth = Depends(get_current_user),
):
    return get_tags(db)


@router.post("", response_model=TagDisplay)
def create(
    request: TagBase,
    db: Session = Depends(get_db),
    # current_user: UserAuth = Depends(get_current_user),
):
    return create_tag(db, request)


@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    # current_user: UserAuth = Depends(get_current_user),
):
    return delete_tag(db, id)
    # return delete_tag(db, id, current_user.id)
