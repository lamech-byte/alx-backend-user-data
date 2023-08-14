from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views
from api.v1.views import index, users

# Register the blueprints
app_views.register_blueprint(index.index)
app_views.register_blueprint(users.users)
