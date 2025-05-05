from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

# Path to the todos.json file
DATA_PATH = 'dat/todos.json'

# Initialize FastAPI app
app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API!"}

# Pydantic model to define the structure of a todo
class Todo(BaseModel):
    task: str
    done: bool = False

# Helper function to read the todos from the JSON file
def read_todos():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r') as f:
            return json.load(f)
    return []

# Helper function to write todos to the JSON file
def write_todos(todos):
    with open(DATA_PATH, 'w') as f:
        json.dump(todos, f, indent=4)

# API Endpoints

@app.get("/todos/")
def get_todos():
    todos = read_todos()
    return todos

@app.post("/todos/")
def add_todo(todo: Todo):
    todos = read_todos()
    new_todo = {"task": todo.task, "done": todo.done}
    todos.append(new_todo)
    write_todos(todos)
    return {"message": "Todo added successfully", "todo": new_todo}

@app.put("/todos/{todo_index}/")
def update_todo(todo_index: int, todo: Todo):
    todos = read_todos()
    if todo_index >= len(todos):
        return {"error": "Todo index out of range"}
    
    todos[todo_index]["task"] = todo.task
    todos[todo_index]["done"] = todo.done
    write_todos(todos)
    return {"message": "Todo updated successfully", "todo": todos[todo_index]}

@app.delete("/todos/{todo_index}/")
def delete_todo(todo_index: int):
    todos = read_todos()
    if todo_index >= len(todos):
        return {"error": "Todo index out of range"}
    
    deleted_todo = todos.pop(todo_index)
    write_todos(todos)
    return {"message": "Todo deleted successfully", "todo": deleted_todo}

# Favicon handling
@app.get("/favicon.ico")
def favicon():
    return {"message": "No favicon available"}
