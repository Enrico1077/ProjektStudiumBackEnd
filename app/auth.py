from flask import jsonify
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from flask_login import UserMixin, login_user

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username
    def getName(user_id):
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT username FROM users WHERE id = %s', (user_id,))
        username = cur.fetchone()[0]
        return User(user_id, username)
    




bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    #Extrahieren der Anmeldedaten und Vorbereiten der DB
    
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']      
    except:
        return jsonify({'error': 'missing parameter'}), 400     

    db = get_db()
    cur = db.cursor()
    error = None

    #Sind Passwort und Nutzername vorhanden?
    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    #Nutzername und Passwort werden der Datenbank hinzugefügt
    if error is None:
        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, generate_password_hash(password)),
            )
            db.commit()

            #Auslesen der User-ID
            cur.execute('SELECT id FROM users WHERE username = %s', (username,))
            user_id = cur.fetchone()[0]

            # Erstellen eines Users und hinzufügen zur Session + returns
            user = User(user_id, username)
            login_user(user)
            return jsonify({'message': 'New user has been created and logged in.'}), 200

        except db.IntegrityError:
            error = f"User {username} is already registered."
    cur.close()

    #Sollte es einen Error geben wird dieser zurückgegeben, sonst wird die erfolgreiche Durchführung mitgeteilt
    if error is None:
        return jsonify({'message': 'New user has been created.'}), 200
    else:
        return jsonify({'error': error}), 400


@bp.route('/login', methods=['POST'])
def login():
    try:
        #Extrahieren der LoginDaten
        login_data = request.get_json()
        username = login_data["username"]
        password = login_data["password"]   

        #Vorbereiten der Datenbank
        db = get_db()
        cur= db.cursor()
        error = None 

        #User mit Username aus der DB suchen
        cur.execute(
            'SELECT * FROM users WHERE username = %s', (username,)
        )
        user = cur.fetchone()

        #Prüfen ob Username und Password korrekt sind
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # Erstellen eines Users und hinzufügen zur Session + returns
            user = User(user['id'], username)
            login_user(user)      
            return (jsonify({'message':'Login has been sucessfull'}),200)
        else:
            return (jsonify({'error':error}),400)

    except: 
        return (jsonify({'error':'unkown error'}),400)
