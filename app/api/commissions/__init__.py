from flask import Blueprint

commissions = Blueprint('commissions', __name__, url_prefix='/api/v1')

from app.api.commissions import urls