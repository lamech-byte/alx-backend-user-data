#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from werkzeug.exceptions import HTTPException, Forbidden
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


if 'AUTH_TYPE' in os.environ:
    if os.environ['AUTH_TYPE'] == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    else:
        auth = Auth()


if 'AUTH_TYPE' in os.environ:
    if os.environ['AUTH_TYPE'] == 'auth':
        from api.v1.auth.auth import Auth
        auth = Auth()

@app.before_request
def before_request():
    if auth:
        required_auth_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
        if request.path not in required_auth_paths and auth.require_auth(request.path, required_auth_paths):
            auth_header = auth.authorization_header(request)
            if auth_header is None:
                abort(401)
            current_user = auth.current_user(request)
            if current_user is None:
                abort(403)

@app.route('/api/v1/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


# Add the error handler for 401 Unauthorized
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized"}), 401


# Add the error handler for 403 Forbidden
@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
