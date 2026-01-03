from flask import Blueprint

# Create admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Import routes to register them with the blueprint
from . import routes
