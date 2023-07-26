#Every file that is not related to authentication

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import  login_required, current_user
from .models import Note 
from . import db
import json

#we can use current_user to access the data the user holds

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST']) #if we go to '/' root it goes to home page
@login_required
def home():
    if request.method=='POST':
        note = request.form.get('note')

        if len(note)<1:
            flash("Note is too short", category='error')
        else:
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added", category='success')
    return render_template('home.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) #we are using json.load since the notes aren't a from and we need the data to be deleted
    #request.data is a string we specified in js as noteId 
    #We are converting it to a python dictionary object
    noteId = note['noteId'] #accessing the noteId from dictionary
    note = Note.query.get(noteId) #getting the noteid 
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({}) #We have to return an empty response



