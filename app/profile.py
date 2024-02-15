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
    username = current_user.username
    
    #Vorbeiten der Datenbank
    db = get_db()
    cur= db.cursor()

    #Ausführen des SQL-Befehls
    cur.execute(
        'SELECT Maschinen_ID FROM BenutzerMaschinen WHERE username = %s', (username,)
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

    

    
