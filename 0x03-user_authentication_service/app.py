#!/usr/bin/env python3
"""
Flask App Module
"""

from flask import Flask, request, jsonify, abort, make_response, redirect
from auth import Auth


app = Flask(__name__)
auth = Auth()


@app.route("/", methods=["GET"])
def hello() -> str:
    """
    Returns a JSON message.

    Returns:
        JSON: Response JSON containing hello message.
            Returns a JSON message.
    """
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route('/users', methods=['POST'])
def register_user():
    """
    POST /users route.
    Register a new user.

    Returns:
        JSON: Response JSON containing user email and creation message.
            If user already exists, returns a JSON message.
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
    Create a new session for a user.

    Args:
        email (str): The user's email.

    Returns:
        Union[str, None]: The session ID if the user exists, else None.
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


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Log out a user by destroying their session.

    Returns:
        Response: A Flask Response with the appropriate
        status code and message.
    """
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)

    if user:
        auth.destroy_session(user.id)
        return redirect('/', code=302)
    else:
        return jsonify({"error": "Forbidden"}), 403


@app.route('/profile', methods=['GET'])
def get_profile():
    """
    Get a new session for user profile.

    Args:
        email (str): The user's email.

    Returns:
        Union[str, None]: The session ID if the user exists, else user not found.
    """
    session_id = request.cookies.get('session_id')
    
    if not session_id:
        return make_response('Session ID is missing', 403)
    
    user = auth.get_user_from_session_id(session_id)
    
    if not user:
        return make_response('Invalid session ID or user not found', 403)
    
    return jsonify({'email': user.email})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
