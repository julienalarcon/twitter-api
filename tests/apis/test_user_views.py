from flask_testing import TestCase
from app import create_app, db
from app.models import User
from unittest.mock import patch

# Used to get a sample for tests
def get_sample_user():
    u = User(username="testuser", id=1, email="testuser@test.com")
    return u


    def test_get_one_invalid_tweet(self, session_mock):
        session_mock.query.return_value.get.return_value = None
        response = self.client.get("/tweets/1")
        self.assertEqual(response.status_code, 404)
        session_mock.query.return_value.get.assert_called_once_with(1)

# TESTS 'GET'
@patch("app.db.session")
class TestUserGetMethod(TestCase):
    # SETUP
    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        return app

    def test_get_one_valid_user(self, session_mock):
        # Mock
        session_mock.query.return_value.get.return_value = get_sample_user()
        # Query
        response = self.client.get("/users/1")
        response_user = response.json
        # Check
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_user["id"], 1)
        self.assertEqual(response_user["username"], "testuser")
        self.assertEqual(response_user["email"], "testuser@test.com")
        session_mock.query.return_value.get.assert_called_once_with(1)

    def test_get_all_users(self, session_mock):
        # Mock
        session_mock.query.return_value.all.return_value = [get_sample_user()]
        # Query
        response = self.client.get("/users")
        response_list = response.json
        # Check
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_list, list)
        self.assertEqual(len(response_list), 1)
        session_mock.query.return_value.all.assert_called_once()

    def test_get_one_invalid_user(self, session_mock):
        # Mock
        session_mock.query.return_value.get.return_value = None
        # Query
        response = self.client.get("/users/1")
        # Check
        self.assertEqual(response.status_code, 404)
        session_mock.query.return_value.get.assert_called_once_with(1)

# TESTS 'POST'
@patch("app.db.session")
class TestUserPostMethod(TestCase):
    # SETUP
    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        return app

    def test_create_one_valid_user(self, session_mock):
        # Payload
        payload = {
            "username": "test",
            "email": "test@test.com",
        }
        # Query
        response = self.client.post("/users", json=payload)
        response_user = response.json
        # Check
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_user["username"], payload["username"])
        self.assertEqual(response_user["email"], payload["email"])
        session_mock.add.assert_called_once()
        session_mock.commit.assert_called_once()

    def test_create_one_user_invalid_payload(self, session_mock):
        # Payload
        payload = {"name": "This is a test"}
        # Query
        response = self.client.post("/users", json=payload)
        # Check
        self.assertEqual(response.status_code, 400)
        session_mock.add.assert_not_called()
        session_mock.commit.assert_not_called()

    def test_create_one_user_no_payload(self, session_mock):
        # Query
        response = self.client.post("/users")
        # Check
        self.assertEqual(response.status_code, 400)
        session_mock.add.assert_not_called()
        session_mock.commit.assert_not_called()

# TESTS 'DELETE'
@patch("app.db.session")
class TestUserDeleteMethod(TestCase):
    # SETUP
    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        return app

    def test_delete_one_user(self, session_mock):
        # mock
        session_mock.query.return_value.get.return_value = get_sample_user()
        # Query
        response = self.client.delete("/users/1")
        # Check
        self.assertEqual(response.status_code, 204)
        session_mock.query.return_value.get.assert_called_once_with(1)
        session_mock.delete.assert_called_once()
        session_mock.commit.assert_called_once()

    def test_delete_one_invalid_user(self, session_mock):
        # Mock
        session_mock.query.return_value.get.return_value = None
        # Query
        response = self.client.delete("/users/1")
        # Check
        self.assertEqual(response.status_code, 404)
        session_mock.query.return_value.get.assert_called_once_with(1)
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()

# TESTS 'DELETE'
@patch("app.db.session")
class TestUserPatchMethod(TestCase):
    # SETUP
    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        return app

    def test_update_one_valid_user(self, session_mock):
        # Mock
        session_mock.query.return_value.get.return_value = get_sample_user()
        # Payload
        payload = {
            "username": "new-user",
            "email": "new-user@new-email.com",
        }
        # Query
        response = self.client.patch("/users/1", json=payload)
        response_user = response.json
        # Check
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_user["username"], payload["username"])
        self.assertEqual(response_user["id"], 1)
        self.assertEqual(response_user["email"], payload["email"])
        session_mock.query.return_value.get.assert_called_once_with(1)
        session_mock.commit.assert_called_once()

    def test_update_one_tweet_no_payload(self, session_mock):
        # Query
        response = self.client.patch("/users/1")
        # Check
        self.assertEqual(response.status_code, 400)
        session_mock.query.return_value.get.assert_not_called()
        session_mock.commit.assert_not_called()
