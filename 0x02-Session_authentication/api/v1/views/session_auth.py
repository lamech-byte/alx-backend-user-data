from flask import Blueprint, request, jsonify
from models.user import User
from api.v1.app import auth

app_views = Blueprint(
    'session_auth', __name__, url_prefix='/api/v1/auth_session'
)


@app_views.route('/login', methods=['POST'], strict_slashes=False)
def session_login():
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
    user_dict = user[0].to_json()

    response = jsonify(user_dict)
    response.set_cookie(auth.session_cookie_name, session_id)

    return response
