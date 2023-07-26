from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"
DB_PATH = r"D:\\Jacob's Documents D Drive\\Learning_Flask\\website" 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jkhkjhkhi' #This is a key for cookies and other private infromation
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(DB_PATH,DB_NAME)}' #We are giving the location of the database
    db.init_app(app)


    #import the variable names from the files
    from .views import views 
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')   
    
    from .models import User, Note
    
    with app.app_context():
        create_database()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #makes sure the login page is open
    login_manager.init_app(app) #initialize application

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #.get looks for the primary key...tells flask to load a user

    return app

def create_database():
    if not path.exists(path.join(DB_PATH, DB_NAME)): 
        db.create_all() #Creating database
        print('Created Database')