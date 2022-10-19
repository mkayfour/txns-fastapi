from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from db.database import get_db
from db.models import DbUser
from .schemas import User, UserLogin
from sqlalchemy.orm.session import Session
from db.hashing import Hash


from jose import JWTError, jwt

SECRET_KEY = "d70c20ddf3fc31173797538a1211668ca17ecf42309a6c40c41547b6057ff2c4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_user(db: Session, request: User):
    new_user = DbUser(
        firstname=request.firstname,
        lastname=request.lastname,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(
    db: Session,
    email: str,
):
    user = db.query(DbUser).filter(DbUser.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found",
        )
    return user


def authenticate_user(db, request: UserLogin):
    user = db.query(DbUser).filter(DbUser.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {request.email} not found",
        )

    if not Hash.verify(user.password, request.password):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Check your email or password",
        )
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class TokenData(BaseModel):
    email: str | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, email: str):
    if email in db:
        user_dict = db[email]
        return UserInDB(**user_dict)


async def get_current_user(
    token: str,
    db: Session = Depends(get_db),
):  # = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"payload: {payload}")
        user = payload.get("user")
        email = user.get("email")
        print(f"email: {email}")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, email=email)
    if user is None:
        raise credentials_exception
    return user
