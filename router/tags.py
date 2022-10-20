from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi import HTTPException, status

from db.database import get_db

from sqlalchemy.orm.session import Session
from db.db_tags import create_tag, delete_tag, get_tags

from db.db_transactions import get_transactions
from db.db_user import get_current_user
from db.schemas import (
    TagBase,
    TagDisplay,
    User,
    UserDisplay,
)


router = APIRouter(prefix="/tag", tags=["tags"])


@router.get("/all", response_model=List[TagDisplay])
def tags(
    db: Session = Depends(get_db),
    current_user: UserDisplay = Depends(get_current_user),
):
    return get_tags(db, current_user)


@router.post(
    "",
    response_model=TagDisplay,
)
def create(
    request: TagBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_tag(db, request, current_user)


@router.delete("/{id}")
def delete(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: UserDisplay = Depends(get_current_user),
):
    return delete_tag(db, tag_id, current_user)
