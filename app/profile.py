from flask import jsonify
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db import get_db
from flask_login import login_required, current_user
bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/test', methods=['POST'])
@login_required
def privateTest():
    return (jsonify({'message':f"hello {current_user.username}, you are signed in."}),200)