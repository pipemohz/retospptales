from flask import request
from app.api.commissions import commissions
from app.core.handlers import CommissionsHandler


@commissions.route('/commissions', methods=['POST'])
def commissions():
    response = CommissionsHandler().run(request)
    return response
