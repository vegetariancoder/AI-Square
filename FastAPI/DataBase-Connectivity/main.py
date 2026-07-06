from fastapi import FastAPI, Depends, status, HTTPException, Path
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from models import Todo, Users
from database import engine, get_db
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(description="Description of the Task", min_length=1,max_length=100,default="No Title")
    description: str = Field(description="Description of the Task", min_length=1,max_length=100,default="No Description")
    priority: int = Field(description="Priority of the book", default=1)
    complete: bool = Field(description="Completed status of the task", default=False)
    owner_id: int = Field(description="Owner id of the task", default=None)

    model_config = {
        'json_schema_extra': {
            'example': {
                'title': 'string',
                'description': 'string',
                'priority': 1,
                'complete': False,
                'owner_id': 'string'
            }
        }
    }



# TODOS
@app.get("/todos",status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency):
    try:
        if len(db.query(Todo).all()) > 0:
            return db.query(Todo).all()
        else:
            return "Table has 0 records"
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.get("/todos/{todo_id}",status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency,todo_id: int = Path(gt=0)):
    try:
        todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
        if todo_model is not None:
            return todo_model
        else:
            return {"message : ID does not exist"}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@app.post("/todos",status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency,todo_request: TodoRequest):
    try:
        todo_model = Todo(**todo_request.model_dump())
        db.add(todo_model)
        db.commit()
        return "Entry created successfully"
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))



# USERS

@app.get("/users",status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency):
    try:
        if len(db.query(Users).all()) > 0:
            return db.query(Users).all()
        else:
            return "Table has 0 records"
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
