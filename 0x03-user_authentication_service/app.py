#!/usr/bin/env python3
"""
Flask App Module
"""

from flask import Flask, jsonify
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
