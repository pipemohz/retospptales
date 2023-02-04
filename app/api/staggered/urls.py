from app.api.staggered import staggered
from flask import request
from app.core.handlers import StaggeredCommisionHandler


@staggered.route('/staggered', methods=['GET', 'POST'])
def staggered():
    response = StaggeredCommisionHandler.run(request)
    return response
