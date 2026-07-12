from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, users
import uvicorn

app = FastAPI(
    title="Todo Application - Pathfinder",
    description="This is an updated description for my application.",
    version="2.0.1"
)

models.Base.metadata.create_all(bind=engine)

app.include_router(todos.router)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
