from flask import Blueprint

# Create reporter blueprint
reporter_bp = Blueprint('reporter', __name__, url_prefix='/reporter')

# Import routes to register them with the blueprint
from . import routes
