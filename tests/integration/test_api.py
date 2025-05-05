import unittest
from fastapi.testclient import TestClient
from backend.main import app

class TestTodoAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.todo = {
            "title": "Test Todo",
            "description": "This is a test",
            "doneStatus": False
        }

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Welcome to the Todo App", response.text)

    def test_create_todo(self):
        response = self.client.post("/todos/", json=self.todo)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)

    def test_update_todo(self):
        # First, create a todo
        create_response = self.client.post("/todos/", json=self.todo)
        todo_id = create_response.json()["id"]

        updated_todo = {
            "title": "Updated",
            "description": "Updated desc",
            "doneStatus": True
        }
        response = self.client.put(f"/todos/{todo_id}", json=updated_todo)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Updated")

    def test_delete_todo(self):
        # First, create a todo
        create_response = self.client.post("/todos/", json=self.todo)
        todo_id = create_response.json()["id"]

        # Then delete it
        response = self.client.delete(f"/todos/{todo_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Todo deleted")

if __name__ == '__main__':
    unittest.main()
