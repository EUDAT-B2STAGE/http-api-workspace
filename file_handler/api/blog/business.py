
"""
Business logic layer for implementing the interface methods.

"""

import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

temp_storage = APP_ROOT = os.path.join(APP_ROOT, 'myworkspace/')

def upload_files(req):
    """
    Uploads one or collection of files.

    """
    if not os.path.isdir(temp_storage):
        os.mkdir(temp_storage)

    for file in req.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join(temp_storage,filename)
        file.save(destination)

def create_collection(data):
    """
    Create a file collection.

    """

