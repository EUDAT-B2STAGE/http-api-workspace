import logging.config

from flask import Flask, Blueprint, session, redirect, url_for, request, jsonify
from file_handler import settings
from file_handler.api.blog.endpoints.registered import ns as registered_namespace
from file_handler.api.blog.endpoints.authentication import ns as authentication_namespace
from file_handler.api.blog.endpoints.authorization import ns as authorization_namespace

from file_handler.api.restplus import api
from file_handler.database import db

from flask_oauthlib.client import OAuth, prepare_request

from base64 import b64encode

#

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
app.secret_key = 'development'
oauth = OAuth(app)

logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

consumer_key = app.config["CONSUMER_KEY"]
consumer_secret = app.config["CONSUMER_SECRET"]

#print("key :", consumer_key)
#print("secret :", consumer_secret)

b2access = oauth.remote_app(
    'b2access',
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    base_url='https://unity.eudat-aai.fz-juelich.de:8443/oauth2/',
    request_token_params={'scope': 'USER_PROFILE GENERATE_USER_CERTIFICATE'},
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://unity.eudat-aai.fz-juelich.de:8443/oauth2/token',
    authorize_url='https://unity.eudat-aai.fz-juelich.de:8443/oauth2-as/oauth2-authz'
)

@app.route('/')
def index():
    if 'b2access_token' in session:
        return 'Logged in. <a href="%s">Log out</a>' % url_for('logout')
    else:
        return 'Not logged in. <a href="%s">Log in</a>' % url_for('login')

@app.route('/login')
def login():
    return b2access.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('b2access_token', None)
    return redirect(url_for('index'))


def decorate_http_request(remote):
    """ Decorate the OAuth call to access token endpoint to inject the Authorization header"""
    old_http_request = remote.http_request
    def new_http_request(uri, headers=None, data=None, method=None):
        if not headers:
            headers = {}
        if not headers.get("Authorization"):
            client_id = remote.consumer_key
            client_secret = remote.consumer_secret
            userpass = b64encode("%s:%s" % (client_id, client_secret)).decode("ascii")
            headers.update({ 'Authorization' : 'Basic %s' %  (userpass,) })
        return old_http_request(uri, headers=headers, data=data, method=method)
    remote.http_request = new_http_request


@app.route('/authorized')
def authorized():
    decorate_http_request(b2access)
    resp = b2access.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    access_token = resp['access_token']
    session['b2access_token'] = (access_token, '')
    if 'origin' in session:
        origin = session['origin']
        session.pop('origin', None)
        # redirect to where the request came from
        return redirect(url_for(origin))
    me = b2access.get('userinfo')
    # print(b2access.get('tokeninfo'))
    # print(me.data)
    return jsonify(me.data)


@b2access.tokengetter
def get_b2access_oauth_token():
    return session.get('b2access_token')


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(authentication_namespace)
    api.add_namespace(registered_namespace)
    api.add_namespace(authorization_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


def main():
    initialize_app(app)
    log.info('** Starting development server at http://{}/api/'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()
