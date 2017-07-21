from flask_restplus import fields
from file_handler.api.restplus import api

collection_name = api.model('Name of the collection', {
    'collection_name': fields.String(required=True, description='Name of the collection to be created.'),
})

rename_content = api.model('Required values for renaming a file', {
    'new_file_name': fields.String(required=True, description='New name of the file'),
    'current_file_name': fields.String(required=True, description='The file to be renamed'),
})

