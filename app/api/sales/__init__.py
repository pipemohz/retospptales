from flask import Blueprint

sales = Blueprint('sales', __name__,url_prefix= '/api/v1')

from app.api.sales import urls