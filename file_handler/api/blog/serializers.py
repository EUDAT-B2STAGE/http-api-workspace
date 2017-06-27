from flask_restplus import fields
from file_handler.api.restplus import api

file_content = api.model('Content of the file', {
    'path': fields.String(required=True, description='Content of the file to be uploaded'),
})

rename_content = api.model('Required values for renaming a file', {
    'newname': fields.String(required=True, description='New name of the file'),
    'resource': fields.String(required=True, description='The resource to be renamed'),
})

