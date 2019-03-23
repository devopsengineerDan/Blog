import os

class Config:
   '''
   App configurations
   '''
   MAIL_SERVER = 'smtp.gmail.com'
   MAIL_PORT = 465
   MAIL_USE_TLS = False
   MAIL_USE_SSL = True
   MAIL_USERNAME = os.environ['EMAIL']
   MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
   UPLOADED_PHOTOS_DEST ='app/static/avatars'
   SQLALCHEMY_DATABASE_URI = os.environ.get('DB_CONNECTION')
   SECRET_KEY = os.environ['SECRET_KEY']

   SIMPLEMDE_JS_IIFE = True
   SIMPLEMDE_USE_CDN = True

class TestConfig(Config):
   SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:Iaa2l.AIs@e,bdI?@localhost/blog_test'
   
class ProdConfig(Config):
   '''
   Docstring goes here
   '''
   # SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
   pass

class DevConfig(Config):
   '''
   Docstring goes here
   '''
   SQLALCHEMY_DATABASE_URI = os.environ.get('DB_CONNECTION')
   DEBUG = True

config_options = {
   'development':DevConfig,
   'production':ProdConfig,
   'test':TestConfig
}