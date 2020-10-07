from unittest import TestCase
from app.models import Tweet
from app.repositories import TweetRepository

class TestRepository(TestCase):
    def setUp(self):
        self.tweet_repository = TweetRepository()

    def test_repository_init_empty_list(self):
        tweets_list = self.tweet_repository.tweets
        self.assertIsInstance(tweets_list, list)
        self.assertEqual(tweets_list, [])

    def test_add_one_tweet(self):
        initial_tweet = Tweet("This is a test")
        one_tweet = self.tweet_repository.add_tweet(initial_tweet)
        tweets_list = self.tweet_repository.tweets
        self.assertEqual(len(tweets_list), 1)
        self.assertIsNotNone(initial_tweet.id)
        self.assertEqual(one_tweet, initial_tweet)

    def test_autoincrement_ids(self):
        first_tweet = Tweet("This is a test")
        self.tweet_repository.add_tweet(first_tweet)
        self.assertEqual(first_tweet.id, 1)
        second_tweet = Tweet("This is a test")
        self.tweet_repository.add_tweet(second_tweet)
        self.assertEqual(second_tweet.id, 2)

    def test_get_one_valid_tweet(self):
        initial_tweet = Tweet("This is a test")
        self.tweet_repository.add_tweet(initial_tweet)
        one_tweet = self.tweet_repository.get_tweet(1)
        self.assertEqual(one_tweet, initial_tweet)

    def test_get_one_invalid_tweet(self):
        one_tweet = self.tweet_repository.get_tweet(1)
        self.assertIsNone(one_tweet)

    def test_delete_one_tweet(self):
        initial_tweet = Tweet("This is a test")
        self.tweet_repository.add_tweet(initial_tweet)
        self.tweet_repository.delete_tweet(1)
        one_tweet = self.tweet_repository.get_tweet(1)
        self.assertIsNone(one_tweet)

    def test_update_one_valid_tweet(self):
        initial_tweet = Tweet("This is a test")
        new_text = "Second test"
        self.tweet_repository.add_tweet(initial_tweet)
        one_tweet_returned = self.tweet_repository.update_tweet(1, text=new_text)
        one_tweet = self.tweet_repository.tweets[0]
        self.assertEqual(one_tweet.text, new_text)
        self.assertEqual(one_tweet, one_tweet_returned)

    def test_update_one_invalid_tweet(self):
        one_tweet = self.tweet_repository.update_tweet(1, text="test")
        self.assertIsNone(one_tweet)

    def test_get_all_tweets(self):
        initial_tweet = Tweet("This is a test")
        self.tweet_repository.add_tweet(initial_tweet)
        all_tweets = self.tweet_repository.get_all_tweets()
        self.assertIsInstance(all_tweets, list)
        self.assertEqual(len(all_tweets), 1)

