import logging

from flask import request
from flask_restplus import Resource
from file_handler.api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('auth', description='log in and out of the REST API')


@ns.route('/login')
class PostsCollection(Resource):

    def post(self):
        """
        Login with basic credentials.
        """

        return None, 201


@ns.route('/logout')
class Logout(Resource):

    @api.response(204, 'logged out successfully deleted.')
    def get(self):
        """
        Logout from current credentials.
        """
        # TODO implement logout.

        return None, 204




