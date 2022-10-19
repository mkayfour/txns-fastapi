from fastapi import HTTPException, status

from db.models import DbTag
from sqlalchemy.orm.session import Session

from db.schemas import TagBase


def get_tags(db: Session):
    return db.query(DbTag).all()


def create_tag(db: Session, request: TagBase):
    new_tag = DbTag(name=request.name, user_id=1)

    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


def delete_tag(db: Session, id: int):
    tag = db.query(DbTag).filter(DbTag.id == id).first()

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with {id} not found",
        )
    db.delete(tag)
    db.commit()
    return "ok"
