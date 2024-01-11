from flask import Flask,request, jsonify, session
from flask_session import Session
from flask_login import LoginManager, login_required
import os


def create_app(test_config=None):
    app= Flask(__name__, instance_relative_config=True) 
    #Session(app)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SESSION_TYPE ='filesystem',
        DB_URL = "dbname=postgres user=postgres password=Test1234 host=34.78.196.208" #local ip: 192.168.0.3
    )

    login_manger = LoginManager()
    login_manger.init_app(app)
    #login_manger.login_view ='/auth/login'


    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.after_request              #Verhindert CORS-Fehler
    def add_headers(response):
        """ Adding some global properties to all response headers """
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With"
        return response
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import profile
    app.register_blueprint(profile.bp)

    @login_manger.user_loader
    def load_user(user_id):
        return auth.User.get(user_id)

    @app.route('/test', methods=['POST'])
    @login_required
    def privateTest():
        return (jsonify({'message':'You are singed in'}),201)


    return app