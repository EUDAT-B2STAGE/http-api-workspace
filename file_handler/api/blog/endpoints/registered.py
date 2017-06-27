import logging

from flask import request
from flask_restplus import Resource
from file_handler.api.blog.business import create_category, delete_category, update_category
from file_handler.api.blog.serializers import category, category_with_posts
from file_handler.api.restplus import api
from file_handler.database.models import Category

log = logging.getLogger(__name__)

ns = api.namespace('api/registered', description='upload, downloads, list and delete objects')


@ns.route('/')
class FileCollection(Resource):

    @api.marshal_list_with(category)
    def get(self):
        """
        Returns a list of files in the collection.
        """
        categories = Category.query.all()
        return categories

    @api.response(200, 'Collection successfully created.')
    @api.response(401, 'Missing or invalid credentials or token')
    @api.expect(category)
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


@ns.route('/<int:id>')
@api.response(404, 'File not found.')
class FileItem(Resource):

    @api.marshal_with(category_with_posts)
    def get(self, id):
        """
        Downloads a single file.
        """
        return Category.query.filter(Category.id == id).one()


    @api.expect(category)
    @api.response(204, 'File successfully uploaded.')
    def put(self, id):
        """
        Uploads a new file.
        """
        data = request.json
        update_category(id, data)
        return None, 204

    @api.response(204, 'File successfully deleted.')
    def delete(self, id):
        """
        Deletes a file.
        """
        delete_category(id)
        return None, 204
