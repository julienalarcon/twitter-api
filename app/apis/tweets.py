# pylint: disable=missing-docstring

from flask_restx import Namespace, Resource, fields
from app.db import tweet_repository

api = Namespace('tweets')
model = api.model('Tweet',
    {
        'id': fields.Integer,
        'text': fields.String,
        'created_at': fields.DateTime,
    }
)

@api.route('/<int:id>')
@api.doc(responses={404: 'Tweet not found'})
@api.param('id', 'The tweet unique identifier')
class TweetResource(Resource):
    @api.marshal_with(model)
    def get(self, id):
        tweet = tweet_repository.get_tweet(id)
        if tweet is None:
            api.abort(404)
        else:
            return tweet
