class TweetRepository():
    def __init__(self):
       self.clear()

    def add_tweet(self, tweet):
        tweet.id = len(self.tweets) + 1
        self.tweets.append(tweet)

    def get_tweet(self, id):
        for t in self.tweets:
            if t.id == id:
                return t

        return None

    def clear(self):
        self.tweets = []
