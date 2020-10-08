from flask_testing import TestCase
from app import create_app, db
from app.models import Tweet

class TestTweetViews(TestCase):
    # SETUP
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f"{app.config['SQLALCHEMY_DATABASE_URI']}_test"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()




    # TESTS 'GET'
    def test_get_one_valid_tweet_api(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        response = self.client.get("/tweets/1")
        response_tweet = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_tweet["id"], 1)
        self.assertEqual(response_tweet["text"], "First tweet")
        self.assertIsNotNone(response_tweet["created_at"])

    def test_get_all_tweets_api(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        response = self.client.get("/tweets")
        response_list = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_list, list)
        self.assertEqual(len(response_list), 1)

    def test_get_one_invalid_tweet_api(self):
        response = self.client.get("/tweets/1")
        self.assertEqual(response.status_code, 404)






    # TESTS 'POST'
    def test_create_one_valid_tweet_api(self):
        payload = {
            "text": "This is a test"
        }
        response = self.client.post("/tweets", json=payload)
        one_tweet = db.session.query(Tweet).get(1)
        one_json_tweet = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(one_json_tweet["text"], payload["text"])
        self.assertEqual(one_json_tweet["id"], 1)
        self.assertIsNotNone(one_tweet) # test that tweet not created in DB

    def test_create_one_tweet_api_invalid_payload(self):
        payload = {
            "name": "This is a test"
        }
        response = self.client.post("/tweets", json=payload)
        one_tweet = db.session.query(Tweet).get(1)
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(one_tweet)

    def test_create_one_tweet_api_empty_payload(self):
        response = self.client.post("/tweets")
        one_tweet = db.session.query(Tweet).get(1)
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(one_tweet)





    # TESTS 'DELETE '
    def test_delete_one_tweet_api(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        response = self.client.delete("/tweets/1")
        one_tweet = db.session.query(Tweet).get(1)
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(one_tweet)

    def test_delete_one_invalid_tweet_api(self):
        response = self.client.delete("/tweets/1")
        self.assertEqual(response.status_code, 404)





    # TESTS 'PATCH'
    def test_update_one_valid_tweet_api(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        payload = {
            "text" : "New text"
        }
        response = self.client.patch("/tweets/1", json=payload)
        one_tweet = db.session.query(Tweet).get(1)
        one_json_tweet = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(one_json_tweet["text"], payload["text"])
        self.assertEqual(one_json_tweet["id"], 1)
        self.assertEqual(one_tweet.text, payload["text"])

    def test_update_one_tweet_api_invalid_payload(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        payload = {
            "name": "New text"
        }
        response = self.client.patch("/tweets/1", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_update_one_tweet_api_empty_payload(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        response = self.client.patch("/tweets/1")
        self.assertEqual(response.status_code, 400)
