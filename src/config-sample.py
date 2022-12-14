# src/config.py

# references the following article from realpython.org
import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))


def _get_bool_env_var(varname, default=None):
    value = os.environ.get(varname, default)

    if value is None:
        return False
    elif isinstance(value, str) and value.lower() == 'false':
        return False
    elif bool(value) is False:
        return False
    else:
        return bool(value)


class BaseConfig(object):
    """Base configuration."""

    # main config
    SECRET_KEY = 'secret_stuff'
    SECURITY_PASSWORD_SALT = 'secret_stuff_salt'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # openai api key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')

    # mail settings
    MAIL_SERVER = os.environ.get('APP_MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('APP_MAIL_PORT', 465))
    MAIL_USE_TLS = _get_bool_env_var('APP_MAIL_USE_TLS', False)
    MAIL_USE_SSL = _get_bool_env_var('APP_MAIL_USE_SSL', True)

    # mail authentication
    MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME', 'your gmail address with 2-step verification enabled')
    MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD', 'your gmail app password')

    # mail accounts
    MAIL_DEFAULT_SENDER = 'your gmail address again'


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'csve.sqlite')
    DEBUG_TB_ENABLED = True


class TestingConfig(BaseConfig):
    """Testing configuration."""
    LOGIN_DISABLED = False
    TESTING = True
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = False

    # To use a SQLite :memory: database, specify an empty URL:
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    DEBUG_TB_ENABLED = False

    SECRET_KEY = None
    SECURITY_PASSWORD_SALT = None

    STRIPE_PUBLISHABLE_KEY = None

    SQLALCHEMY_DATABASE_URI = None

    # production config takes precedence over env variables

    # production config file at ./src/config/production.cfg
    config_path = os.path.join(basedir, 'config', 'production.cfg')

    # if config file exists, read it:
    if os.path.isfile(config_path):
        config = configparser.ConfigParser()

        with open(config_path) as configfile:
            config.read_file(configfile)

        SECRET_KEY = config.get('keys', 'SECRET_KEY')
        SECURITY_PASSWORD_SALT = config.get('keys', 'SECRET_KEY')

        # mail settings
        MAIL_SERVER = config.get('mail', 'MAIL_SERVER')
        MAIL_PORT = config.getint('mail', 'MAIL_PORT')
        MAIL_USE_TLS = config.getboolean('mail', 'MAIL_USE_TLS')
        MAIL_USE_SSL = config.getboolean('mail', 'MAIL_USE_SSL')

        # mail authentication and sender
        MAIL_USERNAME = config.get('mail', 'MAIL_USERNAME')
        MAIL_PASSWORD = config.get('mail', 'MAIL_PASSWORD')
        MAIL_DEFAULT_SENDER = config.get('mail', 'MAIL_DEFAULT_SENDER')

        # database URI
        SQLALCHEMY_DATABASE_URI = config.get('db', 'SQLALCHEMY_DATABASE_URI')

