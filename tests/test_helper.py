import unittest
from unittest.mock import patch
from backend import helper


class TestTodoWithMock(unittest.TestCase):

    @patch("backend.helper.save_list")
    @patch("backend.helper.load_list", return_value=[])
    def test_add_todo(self, mock_load, mock_save):
        todo = helper.add_todo("Mock Title", "Mock Desc", False)
        self.assertEqual(todo["title"], "Mock Title")
        self.assertEqual(todo["description"], "Mock Desc")
        self.assertFalse(todo["doneStatus"])
        self.assertIn("id", todo)
        mock_save.assert_called_once_with([todo])

    @patch("backend.helper.load_list", return_value=[
        {"id": "123", "title": "Sample", "description": "Test", "doneStatus": False}
    ])
    def test_get_todo_details_found(self, mock_load):
        todo = helper.get_todo_details("123")
        self.assertEqual(todo["id"], "123")

    @patch("backend.helper.load_list", return_value=[])
    def test_get_todo_details_not_found(self, mock_load):
        todo = helper.get_todo_details("nonexistent")
        self.assertIsNone(todo)  # since function prints 404 and returns nothing

    @patch("backend.helper.save_list")
    @patch("backend.helper.load_list", return_value=[
        {"id": "123", "title": "Test", "description": "Test", "doneStatus": False}
    ])
    def test_remove_todo_success(self, mock_load, mock_save):
        result = helper.remove_todo("123")
        self.assertTrue(result)
        mock_save.assert_called()

    @patch("backend.helper.save_list")
    @patch("backend.helper.load_list", return_value=[
        {"id": "abc", "title": "X", "description": "Y", "doneStatus": False}
    ])
    def test_update_todo_success(self, mock_load, mock_save):
        result = helper.update_todo("abc", {"title": "Updated"})
        self.assertTrue(result)
        mock_save.assert_called()

    @patch("backend.helper.load_list", return_value=[
        {"id": "not-this", "title": "X", "description": "Y", "doneStatus": False}
    ])
    def test_update_todo_not_found(self, mock_load):
        result = helper.update_todo("missing-id", {"title": "No update"})
        self.assertFalse(result)

    def test_generate_id_unique(self):
        id1 = helper.generate_id()
        id2 = helper.generate_id()
        self.assertNotEqual(id1, id2)
        self.assertEqual(len(id1), 32)


if __name__ == "__main__":
    unittest.main()
