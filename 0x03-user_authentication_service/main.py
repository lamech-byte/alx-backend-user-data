#!/usr/bin/env python3
"""
Main Module for Testing User Authentication Service
"""

import requests
from requests import post

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    Register a new user.
    """
    data = {"email": email, "password": password}
    response = post(f"{BASE_URL}/users", data=data)
    print(
        f"Register User Response: {response.status_code} {response.text}"
    )
    assert response.status_code in (200, 400)


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with incorrect password.
    """
    response = requests.post(
        f"{BASE_URL}/sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 401
    print("Incorrect password login failed.")


def profile_unlogged() -> None:
    """
    Attempt to access profile without logging in.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403
    print("Profile access without login failed.")


def log_in(email: str, password: str) -> str:
    """
    Log in and return the session ID.
    """
    response = requests.post(
        f"{BASE_URL}/sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 200
    session_id = response.json().get("session_id")
    print("Logged in successfully.")
    return session_id


def profile_logged(session_id: str) -> None:
    """
    Access profile after logging in.
    """
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 200
    email = response.json().get("email")
    print(f"Profile of user {email} accessed successfully.")


def log_out(session_id: str) -> None:
    """
    Log out a user.
    """
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.delete(f"{BASE_URL}/sessions", headers=headers)
    assert response.status_code == 302
    print("Logged out successfully.")


def reset_password_token(email: str) -> str:
    """
    Generate a reset password token.
    """
    response = requests.post(
        f"{BASE_URL}/reset_password",
        data={"email": email}
    )
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    print(f"Reset password token generated: {reset_token}")
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update user's password.
    """
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password}
    )
    assert response.status_code == 200
    print("Password updated successfully.")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
