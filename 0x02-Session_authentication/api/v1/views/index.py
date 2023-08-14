#!/usr/bin/env python3
"""
Module of Index views
"""

from flask import jsonify, Blueprint, abort
from werkzeug.exceptions import HTTPException, Unauthorized, Forbidden
from api.v1.views import app_views

# Create a Blueprint for the views
# app_views = Blueprint("app_views", __name__)


@app_views.route('/api/v1/unauthorized', methods=['GET'])
def unauthorized_endpoint():
    """
    Endpoint to raise a 401 Unauthorized error using HTTPException.
    """
    raise Unauthorized(description="Unauthorized")


@app_views.route('/api/v1/forbidden', methods=['GET'])
def forbidden_endpoint():
    """
    Endpoint to raise a 403 Forbidden error using abort.
    """
    abort(403)


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status
    Returns:
      - the status of the API
    """
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats
    Returns:
      - the number of each object
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats), 200


@app_views.route('/', methods=['GET'], strict_slashes=False)
def index():
    return jsonify({"message": "Welcome to the API!"})
