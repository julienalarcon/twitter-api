class TweetRepository():
    def __init__(self):
       self.clear()

    def add_tweet(self, tweet):
        tweet.id = len(self.tweets) + 1
        self.tweets.append(tweet)
        return tweet

    def get_tweet(self, id):
        for t in self.tweets:
            if t.id == id:
                return t

        return None

    def get_all_tweets(self):
        return self.tweets

    def delete_tweet(self, id):
        for i in range(len(self.tweets)):
            if self.tweets[i].id == id:
                del self.tweets[i]
                break

    def update_tweet(self, id, text):
        for i in range(len(self.tweets)):
            if self.tweets[i].id == id:
                self.tweets[i].text = text
                return self.tweets[i]

        return None

    def clear(self):
        self.tweets = []
