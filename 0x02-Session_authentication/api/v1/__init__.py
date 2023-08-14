from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views
from api.v1.views import index, users, session_auth
