from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import mysql.connector
import hashlib
import uvicorn

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="todo_db"
)

# Create a cursor object
cursor = mydb.cursor()

app = FastAPI()

# create the first get endpoint

@app.get("/all_todo_items",status_code=status.HTTP_200_OK)
def get_all_todo_items():
    try:
        cursor.execute("SELECT * FROM todo_list")
        result = cursor.fetchall()
        if len(result) == 0:
            return "No items in the list"
        else:
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("todo-app:app", host="127.0.0.1", port=8000, reload=True)