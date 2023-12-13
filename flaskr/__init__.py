from flask import Flask,request, jsonify
from flask_cors import CORS
import os


def create_app(test_config=None):
    app= Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DB_URL = "dbname=postgres user=postgres password=Test1234 host=34.78.196.208" #local ip: 192.168.0.3
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World"
    
    @app.route("/JsonTest", methods=["Post"])
    def JsTest():
       try:
           js_data= request.get_json()
           response_data={"Hallo":"Ja ist da"}
           return jsonify(response_data),200
       except Exception as e:
           return jsonify({"Hallo":"Ne leider nicht"}),400

    @app.after_request
    def add_headers(response):
        """ Adding some global properties to all response headers """
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-Type'] = 'application/json'
        response.headers['Cache-Control'] = 'no-store'
        return response

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app
