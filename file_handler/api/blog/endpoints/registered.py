import logging

import os

from flask import request, send_from_directory
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
        try:
            print("**Received file upload request: ")
            args = upload_parser.parse_args()
            uploaded_file = args['file']
            filename = secure_filename(uploaded_file.filename)

            if not os.path.isdir(temp_storage):
                os.mkdir(temp_storage)
                print("** Storage location created.")

            file_path = os.path.join(temp_storage,filename)
            uploaded_file.save(file_path)
            print("** File saved to path: ", file_path)
            return "File successfully uploaded.", 200

        except:
            return "Error occured while uploading the file."

    @api.response(200, 'Clean completed.')
    @api.response(401, 'Missing or invalid credentials or token')
    def delete(self):
        """
        Debug clean up. Deletes a collection.
        """

        #TODO Implement Collections deletion - only if debug mode.

        return None, 200


@ns.route('/<string:filename>')
@api.response(401, 'Missing or invalid credentials or token')
class FileItem(Resource):

    @api.response(404, 'File not found.')
    @api.response(200, 'File successfully retrieved.')
    def get(self, filename):
        """
        Downloads a single file.
        """
        print("Request received to download file: ", filename)

        try:
            return send_from_directory(temp_storage, filename)
        except:
            return "Error occured while retrieving the file."


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
