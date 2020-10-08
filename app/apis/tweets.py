# pylint: disable=missing-docstring

from flask import request
from flask_restx import Namespace, Resource, fields
from app.models import Tweet
from app import db

api = Namespace('tweets')
model = api.model('Tweet',
    {
        'id': fields.Integer,
        'text': fields.String,
        'created_at': fields.DateTime,
    }
)

minimum_tweet_field = api.model('MinimumTweetModel', {
    'text': fields.String(description="Tweet Content", required=True)
})

@api.route('')
class TweetMain(Resource):
    @api.doc(responses={400: 'Invalid payload', 200: 'Tweet Created'})
    @api.marshal_with(model, code=200)
    @api.expect(minimum_tweet_field, validate=True)
    def post(self):
        payload = request.json
        tweet = Tweet(text=payload["text"])
        db.session.add(tweet)
        db.session.commit()
        return tweet, 200

    @api.doc(responses={200: 'Success'})
    @api.marshal_with(model, as_list=True, code=200)
    def get(self):
        return db.session.query(Tweet).all(), 200


@api.route('/<int:tweet_id>')
@api.doc(responses={404: 'Tweet not found'})
@api.param('tweet_id', 'The tweet unique identifier')
class TweetById(Resource):
    @api.marshal_with(model, code=200)
    @api.doc(responses={200: 'Tweet Found'})
    def get(self, tweet_id):
        tweet = db.session.query(Tweet).get(tweet_id)
        if tweet is None:
            api.abort(404)
        else:
            return tweet, 200

    @api.marshal_with(model, code=200)
    @api.doc(responses={400: 'Invalid payload', 200: 'Tweet Updated'})
    @api.expect(minimum_tweet_field, validate=True)
    def patch(self, tweet_id):
        payload = request.json
        tweet = db.session.query(Tweet).get(tweet_id)
        tweet.text = payload["text"]
        db.session.commit()

        if tweet is None:
            api.abort(404)
        else:
            return tweet, 200

    @api.doc(responses={ 204: 'Tweet Updated'})
    def delete(self, tweet_id):
        tweet = db.session.query(Tweet).get(tweet_id)

        if tweet is None:
            api.abort(404)

        db.session.delete(tweet)
        db.session.commit()
        return "", 204
