from flask import Flask, request, abort
from flask_login import LoginManager
import os
from datetime import timedelta
from http import HTTPStatus


def create_app(test_config=None):
    app= Flask(__name__, instance_relative_config=True) 
    #Session(app)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SESSION_TYPE ='filesystem',
        DB_URL = "dbname=postgres user=postgres password=Test1234 host=34.78.196.208", #local ip: 192.168.0.3
        ADMIN_NAME ='MainAdmin',
        PERMANENT_SESSION_LIFETIME = timedelta(hours=1),   
        SESSION_COOKIE_HTTPONLY = False,
        SESSION_COOKIE_SAMESITE = 'Lax',
        SESSION_COOKIE_SECURE = True,
        SESSION_COOKIE_DOMAIN =  '.projektstudium.für-den-bachelor.eu'
        #SESSION_COOKIE_DOMAIN = '.localhost'        #For Local Use
    
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
        response.headers["Access-Control-Allow-Origin"] = "https://projektstudium.xn--fr-den-bachelor-zvb.eu"
        #response.headers["Access-Control-Allow-Origin"] = "https://localhost:4200"      #For Local Use
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import profile
    app.register_blueprint(profile.bp)

    from . import Maschine
    app.register_blueprint (Maschine.bp)

    @login_manger.user_loader
    def load_user(user_id):
        return auth.User.getName(user_id)
    
    @login_manger.unauthorized_handler
    def unauthorized():
        abort(HTTPStatus.UNAUTHORIZED)

    @app.route('/hello', methods=['GET']) #Route zum Testen ob der Dienst online ist
    def hello():
        return "I am here ;D" , 200
        


    return app