from flask import request
from app.core.handlers import SalesHandler
from app.api.sales import sales


@sales.route('/sales', methods=['GET'])
def sales():
    response = SalesHandler.run(request)
    return response
