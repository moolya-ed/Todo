import json
import os
import uuid

file_path = 'dat/todos.json'  # Moved outside so all functions can use it

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
            return
    print("Todo not found.")

# Update todo
def update_todo(todo_id, updated_data):
    todos = load_list()
    for todo in todos:
        if todo["id"] == todo_id:
            todo.update(updated_data)  # Only updates the fields provided
            save_list(todos)
            print("Todo updated.")
            return
    print("Todo not found.")

# Generate unique ID
def generate_id():
    return uuid.uuid4().hex

# Add new todo
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
    print("New todo added:")
    print(new_todo)
    return new_todo  # In case we want to use it

# Run and print
todos = load_list()
print(todos)

print(get_todo_details("8af52e54045b423aabaa9bcf7003ff4d"))

save_list(todos)

remove_todo("8af52e54045b423aabaa9bcf7003ff4d")

update_todo("7f3d774efcad4dcbbccd891c2b121860", {
    "title": "Updated Integration Path",
    "doneStatus": True
})

new_id = generate_id()
print("Generated new ID:", new_id)

# Add a new todo
add_todo("New Task", "This task was added using add_todo function", False)
