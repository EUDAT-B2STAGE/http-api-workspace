import logging
import os
import zipfile

from flask import request, send_from_directory
from flask_restplus import Resource, reqparse
from file_handler.api.blog.business import upload_files, create_collection, APP_ROOT
from file_handler.api.blog.serializers import collection_name, rename_content
from file_handler.api.restplus import api

from shutil import make_archive

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

collection_parser = reqparse.RequestParser()
collection_parser.add_argument('collection_name', required=True, location='args')

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=FileStorage, location='files', required=True)

log = logging.getLogger(__name__)

ns = api.namespace('api/workspace', description='upload, downloads, list and delete objects')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

temp_storage = os.path.join(APP_ROOT, 'myworkspace/')

@ns.route('/')
class FileCollection(Resource):

    @api.expect(collection_parser)
    @api.response(200, 'Collection successfully created.')
    @api.response(401, 'Missing or invalid credentials or token')
    def post(self):
        """
        Creates a new collection.
        """

        print("**Received a request to create a new Collection: ")

        try:
            args = collection_parser.parse_args()
            print("Collection is parsed!")
            workspace = args['collection_name']
            print("Collection to be created: ", workspace)

            absFilePath = APP_ROOT + "/" + workspace
            print("Location to be created: ", absFilePath)
            if not os.path.exists(absFilePath):
                os.mkdir(absFilePath)
                print("Location created.")
                return "Collection successfully created.", 200
            else:
               return "Collection already exists", 403

        except:
            return "Error occured while trying to create the collection."

    @api.expect(collection_parser)
    @api.response(200, 'Collection deleted successfully.')
    @api.response(401, 'Missing or invalid credentials or token')
    def delete(self):
        """
        Debug clean up. Deletes a collection.
        """

        print("**Received a request to delete a Collection: ")

        try:
            args = collection_parser.parse_args()
            print("Collection is parsed!")
            workspace = args['collection_name']
            print("Collection to be deleted: ", workspace)

            absFilePath = APP_ROOT + "/" + workspace
            print("Location to be deleted: ", absFilePath)

            #Check if the collection is empty
            if os.listdir(absFilePath):
                return "Collection is *not* empty", 403

            os.rmdir(absFilePath)
            return "Collection is deleted successfully", 200

        except:
            return "Error occured while trying to delete the collection."


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
        try:
            print("Request received to rename a file at: ", location)
            data = request.json
            current_file_name = data["current_file_name"]
            new_file_name = data["new_file_name"]
            print("current_file_name: ", current_file_name)
            print("new_file_name: ", new_file_name)

            workspace = APP_ROOT + "/" + location
            absFilePath = workspace + "/" + current_file_name
            print("**Full current file path", absFilePath)

            if not os.path.exists(absFilePath):
                return "No such file", 404

            newAbsFilePath = os.path.join(workspace, new_file_name)
            print("Full new file path: ", newAbsFilePath)

            os.rename(absFilePath, newAbsFilePath)
            return "File is sucessfully renamed", 200

        except:
         return "An error occured renaming the file"

    @api.expect(upload_parser)
    @api.response(204, 'File successfully uploaded.')
    def put(self, location):
        """
        Uploads a new file.
        """

        try:
            print("**Received file upload request: ")

            absFilePath = APP_ROOT + "/" + location
            print("Checking for dir: ", absFilePath)

            # First check location exists.
            if not os.path.exists(absFilePath):
                return "No such location", 404

            args = upload_parser.parse_args()
            uploaded_file = args['file']
            filename = secure_filename(uploaded_file.filename)

            if not os.path.isdir(absFilePath):
                os.mkdir(absFilePath)
                print("** Storage location created: ", absFilePath)

            file_path = os.path.join(absFilePath,filename)
            uploaded_file.save(file_path)
            print("** File saved to path: ", file_path)
            return "File successfully uploaded.", 200

        except:
            return "Error occured while uploading the file."


    @api.response(404, 'File not found.')
    @api.response(200, 'File successfully deleted.')
    def delete(self, location):
        """
        Deletes a file.
        """

        try:
            absFilePath = APP_ROOT + "/" + location
            print("**Full file path", absFilePath)

            if not os.path.exists(absFilePath):
                return "No such location.", 404

            filename = os.path.basename(absFilePath)
            print("About to delete the file: ", filename)

            #Check location is pointing to file (not a directory)
            if filename == "":
                return "Please provide a filename in the workspace instead of a directory", 404

            os.remove(absFilePath)
            print("File is deleted sucessfully")

            return "File is deleted sucessfully.", 200

        except:
            return "Error occured while trying to delete the file."
