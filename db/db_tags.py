from fastapi import HTTPException, status

from db.models import DbTag
from sqlalchemy.orm.session import Session

from db.schemas import TagBase, User, UserDisplay


def get_tags(db: Session, current_user: UserDisplay):
    tags = db.query(DbTag).filter(DbTag.user == current_user).all()
    return tags


def create_tag(db: Session, request: TagBase, current_user: User):
    new_tag = DbTag(name=request.name, user_id=current_user.id)

    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


def delete_tag(db: Session, tag_id: int, current_user: UserDisplay):
    tag = db.query(DbTag).filter(DbTag.id == tag_id).filter(DbTag.user == current_user).first()

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with {tag_id} not found",
        )
    db.delete(tag)
    db.commit()
    return "ok"
