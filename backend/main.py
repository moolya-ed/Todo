from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from typing import Optional
import os
import json
import uuid


app = FastAPI()


# Paths
file_path = "backend/dat/todos.json"
frontend_folder_path = os.path.join(os.getcwd(), "frontend")
static_folder_path = os.path.join(frontend_folder_path, "static")


# Mount static files (css, js) under /static
app.mount("/static", StaticFiles(directory=static_folder_path), name="static")


# Serve index.html at root "/"
@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = os.path.join(frontend_folder_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return {"detail": "index.html not found"}


# Todo model
class Todo(BaseModel):
    title: str
    description: str
    doneStatus: bool
    id: Optional[str] = None


# Utility functions
def load_list():
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        if content.strip() == "":
            return []
        else:
            return json.loads(content)
    else:
        return []


def save_list(todo_list):
    if os.access(os.path.dirname(file_path), os.W_OK):
        with open(file_path, 'w') as file:
            json.dump(todo_list, file, indent=4)
    else:
        print("Directory not accessible.")


# API endpoints
@app.get("/todos/", response_model=list[Todo])
def get_todos():
    todos = load_list()
    return todos


@app.post("/todos/", response_model=Todo)
def add_todo_api(todo: Todo):
    todo.id = str(uuid.uuid4())  # Generate new ID
    todos = load_list()
    todos.append(todo.model_dump())
    save_list(todos)
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo_api(todo_id: str, updated_data: Todo):
    todos = load_list()
    for todo in todos:
        if todo['id'] == todo_id:
            todo.update(updated_data.model_dump())
            save_list(todos)
            return todo
    return {"error": "Todo not found"}

@app.delete("/todos/{todo_id}")
def delete_todo_api(todo_id: str):
    todos = load_list()
    for todo in todos:
        if todo['id'] == todo_id:
            todos.remove(todo)
            save_list(todos)
            return {"message": "Todo deleted"}  # ✅ Expected by test
    raise HTTPException(status_code=404, detail="Todo not found")  # Proper 404 error
