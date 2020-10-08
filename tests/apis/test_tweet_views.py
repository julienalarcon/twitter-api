from flask_testing import TestCase
from app import create_app, db
from app.models import Tweet, User
from unittest.mock import patch


# Used to get a sample for tests
def get_sample_tweet():
    t = Tweet(text="test", id=1)
    return t

def get_sample_user():
    u = User(username="testuser", id=1, email="testuser@test.com")
    return u

# TESTS 'GET'
@patch("app.db.session")
class TestTweetGetMethod(TestCase):
    # SETUP
    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        return app

    def test_get_one_valid_tweet(self, session_mock):
        # Mock DB
        session_mock.query.return_value.get.return_value = get_sample_tweet()
        # Query
        response = self.client.get("/tweets/1")
        response_tweet = response.json
        # Check
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_tweet["id"], 1)
        self.assertEqual(response_tweet["text"], "test")
        session_mock.query.return_value.get.assert_called_once_with(1)

    def test_get_all_tweets(self, session_mock):
        # Mock DB
        session_mock.query.return_value.all.return_value = [get_sample_tweet()]
        # Query
        response = self.client.get("/tweets")
        response_list = response.json
        # Check
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_list, list)
        self.assertEqual(len(response_list), 1)
        session_mock.query.return_value.all.assert_called_once()

    def test_get_one_invalid_tweet(self, session_mock):
        session_mock.query.return_value.get.return_value = None
        response = self.client.get("/tweets/1")
        self.assertEqual(response.status_code, 404)
        session_mock.query.return_value.get.assert_called_once_with(1)

# TESTS 'POST'
@patch("app.db.session")
class TestTweetPostMethod(TestCase):
    # SETUP
    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        return app

    def test_create_one_valid_tweet(self, session_mock):
        # Mock DB
        session_mock.query.return_value.get.return_value = [get_sample_user(), get_sample_tweet()]
        # Payload
        payload = {
            "text": "This is a test",
            "user_id": 1,
        }
        # Query
        response = self.client.post("/tweets", json=payload)
        response_tweet = response.json
        # Check
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_tweet["text"], payload["text"])
        session_mock.add.assert_called_once()
        session_mock.query.return_value.get.assert_called()
        session_mock.commit.assert_called_once()

    def test_create_one_tweet_invalid_payload(self, session_mock):
        # Payload
        payload = {"name": "This is a test"}
        # Query
        response = self.client.post("/tweets", json=payload)
        # Check
        self.assertEqual(response.status_code, 400)
        session_mock.add.assert_not_called()
        session_mock.commit.assert_not_called()

    def test_create_one_tweet_no_payload(self, session_mock):
        # Query
        response = self.client.post("/tweets")
        # Check
        self.assertEqual(response.status_code, 400)
        session_mock.add.assert_not_called()
        session_mock.commit.assert_not_called()

    def test_create_one_tweet_invalid_user(self, session_mock):
        # Mock
        session_mock.query.return_value.get.return_value = None
        # payload
        payload = {
            "text": "This is a test",
            "user_id": 1,
        }
        # Query
        response = self.client.post("/tweets", json=payload)
        # Check
        self.assertEqual(response.status_code, 400)
        session_mock.add.assert_not_called()
        session_mock.query.return_value.get.assert_called_once_with(1)
        session_mock.commit.assert_not_called()

# TESTS 'DELETE'
@patch("app.db.session")
class TestTweetDeleteMethod(TestCase):
    # SETUP
    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        return app

    def test_delete_one_tweet(self, session_mock):
        # Mock
        t = get_sample_tweet()
        session_mock.query.return_value.get.return_value = t
        # Query
        response = self.client.delete("/tweets/1")
        # Check
        self.assertEqual(response.status_code, 204)
        session_mock.query.return_value.get.assert_called_once_with(1)
        session_mock.delete.assert_called_once_with(t)
        session_mock.commit.assert_called_once()

    def test_delete_one_invalid_tweet(self, session_mock):
        # Mock
        session_mock.query.return_value.get.return_value = None
        # Query
        response = self.client.delete("/tweets/1")
        # Check
        self.assertEqual(response.status_code, 404)
        session_mock.query.return_value.get.assert_called_once_with(1)
        session_mock.delete.assert_not_called()
        session_mock.commit.assert_not_called()

# TESTS 'PATCH'
@patch("app.db.session")
class TestTweetPatchMethod(TestCase):
    # SETUP
    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        return app

    def test_update_one_valid_tweet(self, session_mock):
        # Mock
        session_mock.query.return_value.get.return_value = get_sample_tweet()
        # Payload
        payload = {"text": "New text"}
        # Query
        response = self.client.patch("/tweets/1", json=payload)
        response_tweet = response.json
        # Check
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_tweet["text"], payload["text"])
        self.assertEqual(response_tweet["id"], 1)
        session_mock.query.return_value.get.assert_called_once_with(1)
        session_mock.commit.assert_called_once()

    def test_update_one_tweet_no_payload(self, session_mock):
        # Query
        response = self.client.patch("/tweets/1")
        # Check
        self.assertEqual(response.status_code, 400)
        session_mock.query.return_value.get.assert_not_called()
        session_mock.commit.assert_not_called()

    def test_update_one_invalid_tweet(self, session_mock):
        # Mock
        session_mock.query.return_value.get.return_value = None
        # Query
        response = self.client.patch("/tweets/1", json={"text": "test"})
        # Check
        self.assertEqual(response.status_code, 404)
        session_mock.query.return_value.get.assert_called_once_with(1)
        session_mock.commit.assert_not_called()
