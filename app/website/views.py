from flask import Blueprint, render_template, request,flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        note = request.form.get('note')
        if( len(note)< 5):
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
        
    return render_template("dashboard.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = data['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})