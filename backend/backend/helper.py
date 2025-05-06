import json
import os
import uuid
import logging

# Ensure logs directory exists
os.makedirs('backend/logs', exist_ok=True)

# Set up logging
logging.basicConfig(
    filename='backend/logs/todo.log',  # Log file path
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

file_path = "backend/dat/todos.json"  # Moved outside so all functions can use it

# Load todos from file
def load_list():
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()

        if content.strip() == "":
            logging.info("Todos file is empty.")
            return []
        else:
            try:
                data = json.loads(content)
                logging.info("Todos loaded successfully.")
                return data
            except json.JSONDecodeError as e:
                logging.error(f"Failed to parse JSON: {e}")
                return []
    else:
        logging.warning("Todos file not found.")
        return []

# Get a todo by id
def get_todo_details(todo_id):
    todos = load_list()
    for todo in todos:
        if todo["id"] == str(todo_id):  # ID comparison
            logging.info(f"Todo retrieved: {todo_id}")
            return todo
    logging.warning(f"Todo not found: {todo_id}")
    print("404 not found")


os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Save todos to file
def save_list(todo_list):
    try:
        if os.access(os.path.dirname(file_path), os.W_OK):
            with open(file_path, 'w') as file:
                json.dump(todo_list, file, indent=4)
            logging.info("Todos saved successfully.")
        else:
            logging.error("Directory not accessible for writing.")
            print("Directory not accessible.")
    except Exception as e:
        logging.error(f"Failed to save todos: {e}")

# Remove todo
def remove_todo(todo_id):
    todos = load_list()
    for todo in todos:
        if todo['id'] == todo_id:
            todos.remove(todo)
            save_list(todos)
            logging.info(f"Todo removed: {todo_id}")
            print("Todo removed.")
            return True
    logging.warning(f"Todo to remove not found: {todo_id}")
    print("Todo not found.")
    return

# Update todo
def update_todo(todo_id, updated_data):
    todos = load_list()
    for todo in todos:
        if todo["id"] == todo_id:
            todo.update(updated_data)  # Only updates the fields provided
            save_list(todos)
            logging.info(f"Todo updated: {todo_id}")
            print("Todo updated.")
            return True
    logging.warning(f"Todo to update not found: {todo_id}")
    print("Todo not found.")
    return False

# Generate unique ID
def generate_id():
    new_id = uuid.uuid4().hex
    logging.debug(f"Generated ID: {new_id}")
    return new_id

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
    logging.info(f"Todo added: {new_todo['id']}")
    return new_todo


# Example usage: Calling the functions to add, update, remove, and retrieve todos

# Add some todos
todo1 = add_todo("Learn Python", "Complete the Python course", False)
todo2 = add_todo("Read book", "Read 'Atomic Habits'", True)

# Update a todo
update_todo(todo1['id'], {"doneStatus": True})

# Get todo details
todo_details = get_todo_details(todo1['id'])
print(todo_details)

# Remove a todo
remove_todo(todo2['id'])

# Check if the todo was removed by trying to get it again
todo_details = get_todo_details(todo2['id'])
print(todo_details)
