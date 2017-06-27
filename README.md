EUDAT File Handler
==================

This repository contains a RESTful API based on Flask and Flask-RESTPlus for EUDAT File Handler.

To use the handler, first create a directory and move in to it; for example

    mkdir eudat
    cd eudat

Setup and activate virtualenv:

    virtualenv venv
    source venv/bin/activate

To download the code use:

    git clone https://github.com/charaka1/eudat-file-handler.git

Install the necessary libraries:

    pip install -r requirements.txt

Add the current directory to PYTHONPATH:

    export PYTHONPATH=.:$PYTHONPATH

Start the Python Flask server:

    python file_handler/app.py

Open a web browser and point to http://localhost:5000/api/

You should see the Swagger API.
