from flask import jsonify
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app)
from app.db import get_db
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
bp = Blueprint('Maschine', __name__, url_prefix='/Maschine')


@bp.route('/Upload', methods=['POST'])
#Upload von Maschinendaten, neben den Daten müssen auch Nutzerdaten und MaschinenId mitgegeben werden 
def UploadData():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        maschineId = data['maschineID']      
    except:
        return jsonify({'error': 'Missing Username or Password or MaschineID'}), 400 
    
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
        cur.execute(
            'SELECT * FROM BenutzerMaschinen WHERE Benutzer_ID = %s AND Maschinen_ID = %s',(user['id'], maschineId)
        )
        curMaschine = cur.fetchone()

        if curMaschine is None:
            error = 'The user has no access to the Machine-ID'
        else:
            cur.execute(                #Der SQL-Zugriff muss noch auf die Datenbank abgestimmt werden 
                "INSERT INTO Maschinen (Maschinendata1, Maschinendata2,) VALUES (%s, %s)",
                (data['Maschinedata1'], data['Maschinedata2']),
            )
            db.commit()

    if error is None:
        return jsonify({'message':'Machine data successfully inserted'}),200
    else:
        return jsonify({'error':error}),400



@bp.route('/ConnectMaschine', methods=['POST'])
#Zuweisung von Nutzer und Maschine (Nur durch Admin möglich)
def ConnectMaschine():
    try:
        data = request.get_json()
        adminname = data['adminname']
        adminpassword = data['adminpassword']
        maschineId = data['maschineID'] 
        username = data['username']

    except:
        return jsonify({'error': 'Missing Username or Password or MaschineID'}), 400 
    
    if not adminname == current_app.config['ADMIN_NAME'] :
        return jsonify({'error': 'Adminname is wrong'}), 400 
    
    #Vorbereiten der Datenbank
    db = get_db()
    cur= db.cursor()
    error = None 

    #User mit Adminname aus der DB suchen
    cur.execute(
        'SELECT * FROM users WHERE username = %s', (adminname,)
    )
    adminuser = cur.fetchone()

    #Prüfen ob Adminname und AdminPassword korrekt sind
    if adminuser is None:
        error = 'There is no AdminAccount.'
    elif not check_password_hash(adminuser['password'], adminpassword):
        error = 'Incorrect Adminpassword.'

    #Sucht den Nutzer aus der Tabelle
    cur.execute(
        'SELECT * FROM users WHERE username = %s', (username,)
    )
    user = cur.fetchone()
    if user is None:
        error = 'Username is wrong'
    
    #Sollte es keine Fehler geben, werden Nutzer und Maschine verknüpft
    if error is None:
        cur.execute(          
            "INSERT INTO BenutzerMaschinen (Benutzer_ID, Maschinen_ID) VALUES (%s, %s)",
            (user['id'], maschineId)
            )           
        db.commit()

    #Ausgabe
    if error is None:
        return jsonify({'message':'Link was successful'}),200
    else:
        return jsonify({'error':error}),400

        
