#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint
from api.v1.views import session_auth
from api.v1.views.session_auth import app_views as session_auth_views

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
app_views.register_blueprint(session_auth.app_views)

from api.v1.views.index import *
from api.v1.views.users import *

User.load_from_file()
