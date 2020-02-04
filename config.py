import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    DATABASE_URI = 'postgres://nvkqvsjloowrzm:5629578f94b3ab1f6d965f9d78c59b7dd2c485b2759569548b13f5700b8892e3@ec2-52-203-160-194.compute-1.amazonaws.com:5432/dcpul066frgu79'
    SQLALCHEMY_TRACK_MODIFICATIONS = False