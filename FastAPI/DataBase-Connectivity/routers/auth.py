from datetime import timedelta
from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
router = APIRouter()

SECRET_KEY = "98a5bdd7892cdeefe340f8a05841c003c8c94bbadfa3d8ca87430a137621d2d4"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# database dependency
db_dependency = Annotated[Session, Depends(get_db)]

# OAuth dependency
oauth2_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return True

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    return jwt.encode(
        {"sub": username}, SECRET_KEY, algorithm=ALGORITHM
    )

@router.post("/token",status_code=status.HTTP_200_OK ,tags=["Authentication"])
async def login_for_access_token(form_data: oauth2_dependency, db: db_dependency):
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return "Successful Login"