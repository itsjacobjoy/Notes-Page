from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user

#Hashing Function
# x -> y 
# f(x) = x+1
# f(y) = y-1
# y -> x
#A Hashing function has no inverse
#x -> y
#y -> ?

auth = Blueprint('auth', __name__)

#GET request is when we are retreiving information
#POST request is when changes are being made to a database, etc

@auth.route('/login', methods= ['GET', 'POST'])
def login():
    # data = request.form #request allows you to grab infromation which has all of the data that was sent as part of a form
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() 
        #this is used to query the database...it filters all the users that have an email
        #the first makes sure that the first email matching the specific email is taken...i.e it will as each user will have a unique email

        if user:
            if check_password_hash(user.password, password):
                flash("Login Successful", category='success')
                login_user(user, remember=True) #It remembers the fact that the user is logged in until the web server stops running or user clears their browsing history
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("Email does not exist",category='error')

    return render_template('login.html', user = current_user) #(linked page, any varibale name)

@auth.route('/logout')
@login_required  #This is required to make sure that the user can only logout if the user has logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()  
        if user:
            flash('There is already an account under this email', category='error')
        elif len(email)<4:
            #flash function allows you to display the message, however the conditions need to be defined on the base.html file
            flash('Invalid Email', category='error') #the category variable can be any string you are assigning
        elif len(name) < 2:
            flash("Provide a valid name", category='error')
        elif password1!=password2:
            flash("Passwords do not match", category='error')
        elif len(password1) < 7:
            flash("Password should be greater than 7 characters", category='error')
        else: 
            new_user = User(email=email, name=name,password=generate_password_hash(password1, method='sha256')) #method is a predefined hashing function...it can be anything
            db.session.add(new_user) #Adding to database
            db.session.commit() #Updation confrimation
            login_user(user, remember=True)
            flash('Successfully created an account', category='success')
            return redirect(url_for('views.home'))
            #The () in the url_for function is cooresponding to the python file where the home page function is created(views) and he function where home page is rendered(.home)

    return render_template('sign_up.html', user=current_user)