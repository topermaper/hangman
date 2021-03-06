import os

class BaseConfig(object):
    #Flask Configuration
    # SECRET KEY to be set as environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY','default_key')
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI='sqlite:///database.db'

    # Game configuration
    WORD_LIST = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
    ALLOWED_MISSES = 4

    # API configuration
    TOKEN_EXPIRATION = 3600
    BASE_API_URL     = '/api/v1'

class ProductionConfig(BaseConfig):
    DEBUG = False
    TOKEN_EXPIRATION = 600
    # SECRET KEY to be set as environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(BaseConfig):
    ENV= 'development'
    DEBUG = True
    TESTING = True
