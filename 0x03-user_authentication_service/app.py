#!/usr/bin/env python3
"""
Flask App Module
"""

from flask import Flask, request, jsonify, abort, make_response
from auth import Auth


app = Flask(__name__)
auth = Auth()


@app.route("/", methods=["GET"])
def hello() -> str:
    """
    Returns a JSON message.
    """
    message = {"message": "Bienvenue"}
    return jsonify(message)

@app.route('/users', methods=['POST'])
def register_user():
    """
    POST /users route.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = auth.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'])
def create_session():
    """
    POST /sessions route.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if auth.valid_login(email, password):
        session_id = auth.create_session(email)
        response_data = {"email": email, "message": "logged in"}
        response = jsonify(response_data)
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
