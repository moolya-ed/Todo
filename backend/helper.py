import json
import os
import uuid


file_path = "backend/dat/todos.json"  # Moved outside so all functions can use it


# Load todos from file
def load_list():
   if os.path.exists(file_path):
       with open(file_path, 'r') as file:
           content = file.read()


       if content.strip() == "":
           print("File is empty.")
           return []
       else:
           data = json.loads(content)
           return data
   else:
       print("File not found.")
       return []


# Get a todo by id
def get_todo_details(todo_id):
   todos = load_list()
   for todo in todos:
       if todo["id"] == str(todo_id):  # ID comparison
           return todo
   print("404 not found")


# Save todos to file
def save_list(todo_list):
   if os.access(os.path.dirname(file_path), os.W_OK):
       with open(file_path, 'w') as file:
           json.dump(todo_list, file, indent=4)
       print("Todos saved.")
   else:
       print("Directory not accessible.")


# Remove todo
def remove_todo(todo_id):
   todos = load_list()
   for todo in todos:
       if todo['id'] == todo_id:
           todos.remove(todo)
           save_list(todos)
           print("Todo removed.")
           return True
   print("Todo not found.")
   return 


# Update todo
def update_todo(todo_id, updated_data):
   todos = load_list()
   for todo in todos:
       if todo["id"] == todo_id:
           todo.update(updated_data)  # Only updates the fields provided
           save_list(todos)
           print("Todo updated.")
           return True
   print("Todo not found.")
   return False


# Generate unique ID
def generate_id():
   return uuid.uuid4().hex


def add_todo(title, description, doneStatus):
    new_todo = {
        "title": title,
        "description": description,
        "doneStatus": doneStatus,
        "id": generate_id()
    }
    todos = load_list()
    todos.append(new_todo)
    save_list(todos)
    return new_todo
