from datetime import timedelta, datetime, timezone
from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt,JWTError
router = APIRouter()

SECRET_KEY = "98a5bdd7892cdeefe340f8a05841c003c8c94bbadfa3d8ca87430a137621d2d4"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# database dependency
db_dependency = Annotated[Session, Depends(get_db)]

# OAuth dependency
oauth2_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
oauth2_decode_bearer_dependency = Annotated[str, Depends(oauth2_scheme)]

class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username,'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: oauth2_decode_bearer_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")



@router.post("/token",response_model=Token,status_code=status.HTTP_200_OK ,tags=["Authentication"])
async def login_for_access_token(form_data: oauth2_dependency, db: db_dependency):
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token(username=user.username, user_id=user.id,expires_delta=timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer'}
