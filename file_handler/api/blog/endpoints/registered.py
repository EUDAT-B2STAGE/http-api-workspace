import logging

import os

from flask import request
from flask_restplus import Resource, reqparse
from file_handler.api.blog.business import upload_files, create_collection
from file_handler.api.blog.serializers import file_content, rename_content
from file_handler.api.restplus import api

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=FileStorage, location='files', required=True)

log = logging.getLogger(__name__)

ns = api.namespace('api/registered', description='upload, downloads, list and delete objects')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

temp_storage = APP_ROOT = os.path.join(APP_ROOT, 'myworkspace/')

@ns.route('/')
class FileCollection(Resource):

    @api.response(200, 'Collection successfully created.')
    @api.response(401, 'Missing or invalid credentials or token')
    @api.expect(upload_parser)
    def post(self):
        """
        Creates a new collection.
        """
        print("**Received file upload request: ")
        args = upload_parser.parse_args()
        uploaded_file = args['file']
        filename = secure_filename(uploaded_file.filename)
        print("** Uploaded file: ", filename)

        if not os.path.isdir(temp_storage):
            os.mkdir(temp_storage)
        os.path.join(temp_storage,filename)



        return None, 200

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

    @api.expect(upload_parser)
    @api.response(204, 'File successfully uploaded.')
    def put(self, location):
        """
        Uploads a new file.
        """
        # TODO Use location passed in to store the file.

        print("**Received file upload request: " + location)

        loc = location

        upload_files(request)

        return None, 204

    @api.response(404, 'File not found.')
    @api.response(200, 'File successfully deleted.')
    def delete(self, location):
        """
        Deletes a file.
        """

        return None, 200
