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


def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        Get the User corresponding to a session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            Optional[User]: The corresponding User or None if not found.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
