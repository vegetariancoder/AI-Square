from fastapi import FastAPI, Depends, status, HTTPException
from typing_extensions import Annotated
from sqlalchemy.orm import Session
import models
from models import Todo
from database import engine, get_db
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/todos",status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency):
    try:
        if len(db.query(Todo).all()) > 0:
            return db.query(Todo).all()
        else:
            return "Table has 0 records"
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
