#!/usr/bin/env python3
"""
Session Authentication module
"""

from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth


@app_views.route(
    '/auth_session/login', methods=['POST'], strict_slashes=False
)
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user[0].id)
    response = user[0].to_json()
    response["email"] = user[0].email
    response["id"] = user[0].id
    response["created_at"] = user[0].created_at.strftime(
        '%Y-%m-%d %H:%M:%S'
    )
    response["updated_at"] = user[0].updated_at.strftime(
        '%Y-%m-%d %H:%M:%S'
    )

    return jsonify(response), 200
