from flask import Blueprint

staggered = Blueprint('staggered', __name__, url_prefix='/api/v1')

from app.api.staggered import urls