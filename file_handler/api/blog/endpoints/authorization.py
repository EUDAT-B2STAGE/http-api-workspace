import logging

from flask import request
from flask_restplus import Resource
from file_handler.api.blog.business import create_blog_post, update_post, delete_post
from file_handler.api.blog.serializers import blog_post, page_of_blog_posts
from file_handler.api.blog.parsers import pagination_arguments
from file_handler.api.restplus import api
from file_handler.database.models import Post

log = logging.getLogger(__name__)

ns = api.namespace('auth', description='request and refresh authorization from the B2ACCESS service')


@ns.route('/authorize')
class Authorizer(Resource):

    @api.response(204, 'authorization successful.')
    def get(self):
        """
        Produce internal token if B2ACCESS authorization is granted.
        """
        # TODO implement authorization.

        return None, 204


@ns.route('/askauth')
class Authorizer(Resource):

    @api.response(204, 'authorization successful.')
    def get(self):
        """
        Redirection to B2ACCESS oauth2 login.
        """
        # TODO implement authorization.

        return None, 204


@ns.route('/proxy')
class ProxyManager(Resource):

    @api.expect(blog_post)
    def post(self):
        """
        Check and/or refresh current B2ACCESS proxy credentials.
        """
        create_blog_post(request.json)
        return None, 201







