import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'postgres://rmznaavyfhojnb:64ff65811f3d615605ea0c9c577cf7b5bb94f61361a78d0661cfc2ef337a4cd7@ec2-3-230-106-126.compute-1.amazonaws.com:5432/d2q5u3jbocnmd9'
    SQLALCHEMY_TRACK_MODIFICATIONS = False