import logging

from flask import request
from flask_restplus import Resource
from file_handler.api.restplus import api

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

    def post(self):
        """
        Check and/or refresh current B2ACCESS proxy credentials.
        """

        return None, 201







