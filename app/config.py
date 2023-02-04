import os
import tempfile

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')\
        or os.environ.get('SECRET_KEY')\
        or '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or \
        "IBQj^J9(HEAf#v0l'dvsdK3JcM4*ET"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    JSON_ADD_STATUS = False
    JSON_SORT_KEYS = False
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(tempfile.gettempdir(), 'session_cache')
    SESSION_FILE_THRESHOLD = 100

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'portfolios.db')
    PRODUCTION = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
