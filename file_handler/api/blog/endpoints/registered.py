import logging
import os
import zipfile

from flask import request, send_from_directory, send_file
from flask_restplus import Resource, reqparse
from file_handler.api.blog.business import upload_files, create_collection, APP_ROOT
from file_handler.api.blog.serializers import file_content, rename_content
from file_handler.api.restplus import api

from shutil import make_archive

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=FileStorage, location='files', required=True)

log = logging.getLogger(__name__)

ns = api.namespace('api/registered', description='upload, downloads, list and delete objects')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

temp_storage = os.path.join(APP_ROOT, 'myworkspace/')

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


@ns.route('/<path:location>')
@api.response(401, 'Missing or invalid credentials or token')
class FileItem(Resource):

    @api.response(200, 'File successfully retrieved.')
    def get(self, location):
        """
        Downloads a single file or zipped multiple files in a directory.
        """
        print("Request received to download file: ", location)

        try:
            absFilePath = APP_ROOT + "/" + location
            print("**Full file path", absFilePath)

            if not os.path.exists(absFilePath):
                return "No such location.", 404

            filename = os.path.basename(absFilePath)
            print("** Filename: ", filename)

            if filename == '':
                # Likely to be looking for a directory
                print("Requesting files in a directory")

                # zip the directory and send as a single file
                zipFileName = "workspace.zip"
                zipDir = os.path.dirname(os.path.abspath(absFilePath))
                print("Zip Dir: ", zipDir)
                fullZipFileName = os.path.join(zipDir, zipFileName)
                print("Full zip file name: ", fullZipFileName)

                if os.path.isfile(fullZipFileName):
                    print("Removing the existing zip file")
                    os.remove(fullZipFileName)

                zFile = zipfile.ZipFile(fullZipFileName, 'w', zipfile.ZIP_DEFLATED)
                #listOfFiles = os.listdir(absFilePath)
                for root, dirs, files in os.walk(absFilePath):
                   for file in files:
                       print("Adding file: ", file)
                       zFile.write(absFilePath+file)
                print("Zip file generated")
                return send_from_directory(zipDir, zipFileName)
                #os.remove(fullZipFileName)

            else:
                print("Requesting a single file in a directory.")

                dirName = os.path.dirname(os.path.abspath(absFilePath))
                print("** Directory name: ", dirName)
                return send_from_directory(dirName, filename)
        except:
            return "File not found.", 404



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
