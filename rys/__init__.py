import logging
import azure.functions as func
import os
from app.api import create_app


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)
