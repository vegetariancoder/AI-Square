from fastapi import APIRouter, Depends, status, HTTPException, Path
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Todo, Users
from database import get_db
from routers import auth
from .auth import get_current_user

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
router.include_router(auth.router)


class TodoRequest(BaseModel):
    """
    Represents a TodoRequest model for managing task-related information.

    The TodoRequest class is designed to encapsulate task details including a title,
    description, priority, completion status, and ownership information. This model
    is used to standardize the handling of task data within the application. It also
    includes validation constraints to ensure the integrity of the data.

    :ivar title: Description of the task.
    :type title: str

    :ivar description: Detailed description of the task.
    :type description: str
    :ivar priority: Priority level of the task.
    :type priority: int
    :ivar complete: Indicates whether the task is completed.
    :type complete: bool
    :ivar owner_id: Identifier for the owner of the task.
    :type owner_id: int
    """
    title: str = Field(description="Description of the Task", min_length=1,max_length=100,default="No Title")
    description: str = Field(description="Description of the Task", min_length=1,max_length=100,default="No Description")
    priority: int = Field(description="Priority of the book", default=1)
    complete: bool = Field(description="Completed status of the task", default=False)
    owner_id: int = Field(description="Owner id of the task", default=None)

    model_config = {
        'json_schema_extra': {
            'example': {
                'title': 'Title of the task',
                'description': 'Description of the task',
                'priority': 1,
                'complete': "Pass 0 or 1 (True or False)",
                'owner_id': 'Owner ID of the task - Pass number',
            }
        }
    }
# TODOS
@router.get("/todos",status_code=status.HTTP_200_OK,tags=["Todo"])
async def get_all_todos(user: user_dependency, db: db_dependency):
    """
    Retrieves all Todos items from the database.

    This asynchronous function fetches all entries in the Todos table. If there are
    records in the table, they will be returned. If the table is empty, a string
    indicating that there are no records will be returned. In the event of an
    unexpected error, an HTTPException with a 500 status code and error details
    will be raised.

    :param db: Database dependency used to interact with the database.
    :type db: db_dependency
    :return: A list of Todos items if records exist, otherwise a string indicating
        that the table has 0 records.
    :rtype: Union[List[Todos], str]
    :raises HTTPException: If a database or other internal exception occurs.
    """
    try:
        if len(db.query(Todo).all()) > 0:
            return db.query(Todo).filter(Todo.owner_id == user.get('id')).all()
        else:
            return "Table has 0 records"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/todos/{todo_id}",status_code=status.HTTP_200_OK,tags=["Todo"])
async def get_todo_by_id(user: user_dependency, db: db_dependency,todo_id: int = Path(gt=0)):
    try:
        if user is None:
            raise HTTPException(status_code=401,detail="Authentication Failed")

        todo_model = db.query(Todo).filter(Todo.id == todo_id)\
            .filter(Todo.owner_id == user.get('id'))\
            .first()
        if todo_model is not None:
            return todo_model
        else:
            return {"message : Todo Does Not Exist For This User With ID : " + str(todo_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add_todo",status_code=status.HTTP_201_CREATED,tags=["Todo"])
async def create_todo(user : user_dependency, db: db_dependency,todo_request: TodoRequest):
    try:
        if user is None:
            raise HTTPException(status_code=401,detail="Authentication Failed")
        todo_model = Todo(**todo_request.model_dump())
        db.add(todo_model)
        db.commit()
        return "Entry created successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT,tags=["Todo"])
async def update_todo(user : user_dependency,db: db_dependency,todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail=str(todo_id)+" does not exist")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    # check if owner_id is provided in the request exists in the database
    if todo_request.owner_id is not None:
        user_exists = db.query(Users).filter(Users.id == todo_request.owner_id).first()
        if user_exists is None:
            raise HTTPException(status_code=404, detail=f"Owner with ID {todo_request.owner_id} does not exist")
        todo_model.owner_id = todo_request.owner_id
    db.commit()
    return "Todo updated successfully"

@router.delete("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT,tags=["Todo"])
async def delete_todo(user : user_dependency, db: db_dependency,todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail=" Todo with ID : " +str(todo_id)+" Does Not Exist For This User")
    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()
    return {"message":"todo deleted successfully"}
