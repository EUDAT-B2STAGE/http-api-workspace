import logging

from flask import request
from flask_restplus import Resource
from file_handler.api.blog.business import create_blog_post, update_post, delete_post
from file_handler.api.blog.serializers import blog_post, page_of_blog_posts
from file_handler.api.blog.parsers import pagination_arguments
from file_handler.api.restplus import api
from file_handler.database.models import Post

log = logging.getLogger(__name__)

ns = api.namespace('auth', description='log in and out of the REST API')


@ns.route('/login')
class PostsCollection(Resource):

    @api.expect(blog_post)
    def post(self):
        """
        Login with basic credentials.
        """
        create_blog_post(request.json)
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




