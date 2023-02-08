from datetime import timedelta
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm.session import Session

from db.database import get_db
from db.schemas import TokenResponse, User, UserDisplay, UserLogin
from app.db.db_user import get_user_by_username


from db.db_user import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    create_user,
    get_current_user,
)


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserDisplay)
def create_new_user(request: User, db: Session = Depends(get_db)):
    user = get_user_by_username(db, request.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {request.email} already exists",
        )
    return create_user(db, request)


@router.post("/login", response_model=TokenResponse)
def login_user(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, request)
    json_compatible_user = jsonable_encoder(user)

    # TODO: Is there a better way to do this?
    del json_compatible_user["password"]
    del json_compatible_user["id"]

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user": json_compatible_user}, expires_delta=access_token_expires
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": access_token, "token_type": "bearer"},
    )


@router.get("/users/me/", response_model=UserDisplay)
async def read_users_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return current_user
