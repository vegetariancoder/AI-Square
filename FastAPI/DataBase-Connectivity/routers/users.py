from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db_dependency = Annotated[Session, Depends(get_db)]

class UsersRequest(BaseModel):
    email: str = Field(description="Email of the user", min_length=1,max_length=100,default="No Description")
    username: str = Field(description="username", min_length=1,max_length=10)
    first_name: str = Field(description="First Name of the User", min_length=1,max_length=10)
    last_name: str = Field(description="Last Name of the User", min_length=1,max_length=10)
    password: str = Field(description="Hashed Password", default=None)
    is_active: int = Field(description="Is active Flag", default=0)
    role: str = Field(description="Users Role", min_length=1,max_length=10)

    model_config = {
        'json_schema_extra': {
            'example': {
                'email': 'astha@gmail.com',
                'username': 'astha',
                'first_name': 'astha',
                'last_name': 'nagpal',
                'password': 'mySecurePassword123',
                'is_active': 0,
                'role': 'Developer'
            }
        }
    }

@router.get("/all_users_info",tags=["Users"],summary="Get all users info from the database")
async def get_all_user_info(db: db_dependency):
    try:
        if len(db.query(Users).all()) > 0:
            return db.query(Users).all()
        else:
            return "Table has 0 records"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add_user",status_code=status.HTTP_201_CREATED,tags=["Users"])
async def create_user(db: db_dependency,user_request: UsersRequest):
    try:
        user_data = user_request.model_dump()
        user_data["password"] = bcrypt_context.hash(user_data["password"])
        user_model = Users(**user_data)
        db.add(user_model)
        db.commit()
        return "User created successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))