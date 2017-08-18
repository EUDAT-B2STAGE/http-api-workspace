EUDAT File/Workspace Handler
============================

This repository contains a prototype RESTful web service for EUDAT File/Workspace Handler based on
Flask and Flask-RESTPlus extension. Flask-RESTPlus extention is used for generating the Swagger API.
Since Flask-RESTPlus requires Python 2.7, this implementation is only tested with Python 2.7.

Note that this is just a prototype developed to capture requirements and behaviour of a workspace handler
for EUDAT CDI. Please do *not* get too distracted with the particular technologies used. instead, please
*do* focus on on whether the REST API is suitable for typical usage of such workspace handler. Also, please
do comment on status codes returned and the behaviour.

To use the handler, first create a directory and move in to it; for example

    mkdir eudat
    cd eudat

Setup and activate virtualenv:

    virtualenv venv
    source venv/bin/activate

To download the code use:

    git clone https://github.com/charaka1/eudat-file-handler.git

Move to the file handler base directory:

    cd eudat-file-handler/

Install the necessary libraries:

    pip install -r requirements.txt

Add the current directory to PYTHONPATH:

    export PYTHONPATH=.:$PYTHONPATH

Start the Python Flask server:

    python file_handler/app.py

Open a web browser and point to http://localhost:5000/api/

You should see the Swagger API.

Run the system tests to check that the Workspace interface works as expected.
On a separate command shell move to the file handler base directory, i.e.:

    eudat/file-handler

Then run the nosetests:

    nosetests -v

These system tests also serve as examples of how to use the Workspace API.
