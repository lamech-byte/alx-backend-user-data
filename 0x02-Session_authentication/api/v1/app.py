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
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if 'AUTH_TYPE' in os.environ:
    if os.environ['AUTH_TYPE'] == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif os.environ['AUTH_TYPE'] == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    elif os.environ['AUTH_TYPE'] == 'session_exp_auth':  # Add this elif block
        from api.v1.auth.session_exp_auth import SessionExpAuth
        auth = SessionExpAuth()
    else:
        auth = Auth()


@app.before_request
def before_request():
    """
    Before request handler to perform authentication and authorization checks.
    """
    if auth:
        excluded_paths = [
            '/api/v1/status',
            '/api/v1/unauthorized',
            '/api/v1/forbidden',
            '/api/v1/auth_session/login'  # Add this line
        ]
        if request.path not in excluded_paths and auth.require_auth(
            request.path, excluded_paths
        ):
            auth_header = auth.authorization_header(request)
            if auth_header is None:
                abort(401)
            current_user = auth.current_user(request)
            if current_user is None:
                abort(403)


@app.route('/api/v1/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Status endpoint to return the status of the API.
    """
    return jsonify({"status": "OK"})


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Error handler for 404 Not Found.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """
    Error handler for 401 Unauthorized.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """
    Error handler for 403 Forbidden.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
