import logging

from flask import request
from flask_restplus import Resource
from file_handler.api.blog.business import create_category, delete_category, update_category
from file_handler.api.blog.serializers import file_content, rename_content
from file_handler.api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('api/registered', description='upload, downloads, list and delete objects')


@ns.route('/')
class FileCollection(Resource):

    @api.response(200, 'Collection successfully created.')
    @api.response(401, 'Missing or invalid credentials or token')
    @api.expect(file_content)
    def post(self):
        """
        Creates a new collection.
        """
        data = request.json
        create_category(data)
        return None, 201

    @api.response(200, 'Clean completed.')
    @api.response(401, 'Missing or invalid credentials or token')
    def delete(self):
        """
        Debug clean up. Deletes a collection.
        """

        #TODO Implement Collections deletion - only if debug mode.

        return None, 200


@ns.route('/<string:location>')
@api.response(401, 'Missing or invalid credentials or token')
class FileItem(Resource):

    @api.response(404, 'File not found.')
    @api.response(200, 'File successfully retrieved.')
    def get(self, location):
        """
        Downloads a single file.
        """
        return None, 200

    @api.expect(rename_content)
    @api.response(200, 'File name successfully updated.')
    def patch(self, location):
        """
        Renames a file.

        """
        return None, 200


    @api.expect(file_content)
    @api.response(204, 'File successfully uploaded.')
    def put(self, location):
        """
        Uploads a new file.
        """
        data = request.json
        update_category(id, data)
        return None, 204

    @api.response(404, 'File not found.')
    @api.response(200, 'File successfully deleted.')
    def delete(self, location):
        """
        Deletes a file.
        """
        delete_category(id)
        return None, 200
