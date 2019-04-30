import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mugambi254:pitchdb@localhost/devgarage_test'


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mugambi254:pitchdb@localhost/devgarageblog'
    DEBUG = True

config_options = {"production": ProdConfig,
                  "development": DevConfig, "test": TestConfig}
