from flask_testing import TestCase
from app import create_app, db
from app.models import User


class TestTweetViews(TestCase):
    # SETUP
    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = f"{app.config['SQLALCHEMY_DATABASE_URI']}_test"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_new_user(self):
        first_user = User(username="test", email="test@test.com")
        db.session.add(first_user)
        db.session.commit()

    # TESTS 'GET'
    def test_get_one_valid_user_api(self):
        self.create_new_user()
        response = self.client.get("/users/1")
        response_user = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_user["id"], 1)
        self.assertEqual(response_user["username"], "test")
        self.assertEqual(response_user["email"], "test@test.com")

    def test_get_all_users_api(self):
        self.create_new_user()
        response = self.client.get("/users")
        response_list = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_list, list)
        self.assertEqual(len(response_list), 1)

    def test_get_one_invalid_user_api(self):
        response = self.client.get("/users/1")
        self.assertEqual(response.status_code, 404)

    # TESTS 'POST'
    def test_create_one_valid_user_api(self):
        payload = {
            "username": "test",
            "email": "test@test.com",
        }
        response = self.client.post("/users", json=payload)
        one_user = db.session.query(User).get(1)
        one_json_user = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(one_json_user["username"], payload["username"])
        self.assertEqual(one_json_user["email"], payload["email"])
        self.assertEqual(one_json_user["id"], 1)
        self.assertIsNotNone(one_user)  # test that user created in DB

    def test_create_one_user_api_invalid_payload(self):
        payload = {"name": "This is a test"}
        response = self.client.post("/users", json=payload)
        one_user = db.session.query(User).get(1)
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(one_user)

    def test_create_one_user_api_empty_payload(self):
        response = self.client.post("/users")
        one_user = db.session.query(User).get(1)
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(one_user)

    # TESTS 'DELETE '
    def test_delete_one_user_api(self):
        self.create_new_user()
        response = self.client.delete("/users/1")
        one_user = db.session.query(User).get(1)
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(one_user)

    def test_delete_one_invalid_user_api(self):
        response = self.client.delete("/users/1")
        self.assertEqual(response.status_code, 404)

    # TESTS 'PATCH'
    def test_update_one_valid_user_api(self):
        self.create_new_user()
        payload = {
            "username": "new-user",
            "email": "new-user@new-email.com",
        }
        response = self.client.patch("/users/1", json=payload)
        one_user = db.session.query(User).get(1)
        one_json_user = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(one_json_user["username"], payload["username"])
        self.assertEqual(one_json_user["id"], 1)
        self.assertEqual(one_json_user["email"], payload["email"])
        self.assertEqual(one_user.username, payload["username"])
        self.assertEqual(one_user.email, payload["email"])

    def test_update_one_tweet_api_empty_payload(self):
        self.create_new_user()
        response = self.client.patch("/users/1")
        self.assertEqual(response.status_code, 400)
