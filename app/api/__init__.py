from flask import Flask
from flask_json import FlaskJSON
from app.config import config
from flask_session import Session

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    FlaskJSON(app)
    Session(app)

    from app.api.main import main as main_blueprint
    from app.api.sales import sales as sales_blueprint
    from app.api.commissions import commissions

    app.register_blueprint(main_blueprint)
    app.register_blueprint(sales_blueprint)
    app.register_blueprint(commissions)

    return app
