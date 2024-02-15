from flask import jsonify
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db import get_db
from flask_login import login_required, current_user
bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/test', methods=['POST'])
@login_required
def privateTest():
    return (jsonify({'message':f"hello {current_user.username}, you are signed in."}),200)


@bp.route('/getMaschines', methods=['POST'])
@login_required
def get_maschinen():
    username=current_user.username
    
    #Vorbeiten der Datenbank
    db = get_db()
    cur= db.cursor()

    cur.execute(
        'SELECT id FROM users WHERE username = %s', (username,)
    )
    userID=cur.fetchone()[0]

    #Ausführen des SQL-Befehls
    cur.execute(
        'SELECT Maschinen_ID FROM BenutzerMaschinen WHERE Benutzer_ID = %s', (userID,)
    )
    user_machines = cur.fetchall()
    #Sollten dem Nutzer keine Maschinen zugewiesen worden sein, wird das so zurückgegeben
    if not user_machines:
        return (jsonify({'message':f'{username} has no Maschines assigned!'})), 200
    
    #Die MaschinenIds werden als JSON formatiert und zurückgegeben
    machines_dict = {}
    for i, machine in enumerate(user_machines, start=1):
        machines_dict[f'Machine{i}'] = machine[0]
    return jsonify(machines_dict), 200

    

@bp.route('/getMaschineData', methods=['POST'])
@login_required
def get_machine_data():
    username = current_user.username

    data = request.get_json()
    try:
        machine_id =  data['MachineID']
    except:
        return jsonify({"error": "Missing argument(MachineID)"}), 400

    #Überprüfen ob die Maschine dem User gehört
    db = get_db()
    cur = db.cursor()
    cur.execute('''
                SELECT * FROM BenutzerMaschinen WHERE Benutzer_ID IN (
                            SELECT ID FROM users WHERE username = %s
                         ) AND Maschinen_ID = %s;
               ''', (username, machine_id))
    result = cur.fetchone()
    if not result:
        return jsonify({"message": f"This Machine doesn't belong to {username}!"}), 200
    
    #Daten der Maschine auslesen und zurückgeben
    cur.execute(
        'SELECT UploadTime, Daten FROM Maschinendaten WHERE Maschinen_ID = %s',(machine_id,)
    )
    daten = cur.fetchall()
    print(daten)
    if not daten:
        return (jsonify({'message':f'Die Maschine mit der ID {machine_id} hat keine Daten aufgezeichnet'})), 200
    return(jsonify(daten),200)


