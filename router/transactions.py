from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm.session import Session

from db.database import get_db
from db.db_transactions import create_transaction
from db.db_transactions import delete_transaction
from db.db_transactions import get_transactions
from db.schemas import TransactionBase
from db.schemas import TransactionDisplay


router = APIRouter(prefix="/transaction", tags=["transactions"])


@router.get("/all", response_model=List[TransactionDisplay])
def posts(
    db: Session = Depends(get_db),
    # current_user: UserAuth = Depends(get_current_user),
):
    return get_transactions(db)


@router.post("", response_model=TransactionDisplay)
def create(
    request: TransactionBase,
    db: Session = Depends(get_db),
    # current_user: UserAuth = Depends(get_current_user),
):
    return create_transaction(db, request)


@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    # current_user: UserAuth = Depends(get_current_user),
):
    return delete_transaction(db, id)


# @router.post("/image")
# def upload_file(image: UploadFile = File(...)):
#     letter = string.ascii_letters
#     rand_str = "".join(random.choice(letter) for i in range(6))
#     new = f"_{rand_str}."
#     filename = new.join(image.filename.rsplit(".", 1))
#     path = f"images/{filename}"

#     with open(path, "w+b") as buffer:
#         shutil.copyfileobj(image.file, buffer)

#     return {"filename": path}
