# pylint: disable=missing-docstring

from flask import request
from flask_restx import Namespace, Resource, fields
from app.db import tweet_repository
from app.models import Tweet

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
        tweet = Tweet(payload["text"])
        return tweet_repository.add_tweet(tweet), 200

    @api.doc(responses={200: 'Success'})
    @api.marshal_with(model, as_list=True, code=200)
    def get(self):
        return tweet_repository.get_all_tweets(), 200


@api.route('/<int:id>')
@api.doc(responses={404: 'Tweet not found'})
@api.param('id', 'The tweet unique identifier')
class TweetById(Resource):
    @api.marshal_with(model, code=200)
    @api.doc(responses={200: 'Tweet Found'})
    def get(self, id):
        tweet = tweet_repository.get_tweet(id)
        if tweet is None:
            api.abort(404)
        else:
            return tweet, 200

    @api.marshal_with(model, code=200)
    @api.doc(responses={400: 'Invalid payload', 200: 'Tweet Updated'})
    @api.expect(minimum_tweet_field, validate=True)
    def patch(self, id):
        payload = request.json
        tweet = tweet_repository.update_tweet(id, payload["text"])
        if tweet is None:
            api.abort(404)
        else:
            return tweet, 200

    @api.doc(responses={ 204: 'Tweet Updated'})
    def delete(self, id):
        if tweet_repository.get_tweet(id) is None:
            api.abort(404)

        tweet_repository.delete_tweet(id)
        return "", 204
