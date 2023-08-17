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
        Union[str, None]: The session ID if the user
        exists, else user not found.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        return make_response('Session ID is missing', 403)

    user = auth.get_user_from_session_id(session_id)

    if not user:
        return make_response('Invalid session ID or user not found', 403)

    return jsonify({'email': user.email})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Reset password token for user.

    Args:
        reset password token.

    Returns:
        Union[str, None]: User email if the user
        email does not exists, else missing email field.
    """
    if 'email' not in request.form:
        abort(400, 'Missing email field')

    email = request.form['email']

    try:
        reset_token = auth.get_reset_password_token(email)
        response_data = {
            "email": email,
            "reset_token": reset_token
        }
        return jsonify(response_data), 200
    except ValueError as e:
        abort(403, str(e))


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    Update password token for user.

    Args:
        update user password.

    Returns:
        Union[str, None]: User email if the user
        email does not exists, else invalid reset token.
    """
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
        
        auth.update_password(reset_token, new_password)
        
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        return "Invalid reset token", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
