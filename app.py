from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
db=SQLAlchemy()
def create_app():
    app=Flask(__name__,template_folder="templates")
    app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')


    #postgresql://nikhil_blog_user:ik6DAAMSu8oAwGPqYnuKFOF0hKHO9WhF@dpg-cs0cvp23esus73906u2g-a.oregon-postgres.render.com/nikhil_blog
    app.secret_key="SOME KEY"
    db.init_app(app)
    login_manager=LoginManager()
    login_manager.init_app(app)
    from models import Users
    
    @login_manager.user_loader
    def load_user(uid):
        return Users.query.get(uid)

    bcrypt=Bcrypt(app)

    from routes import register_routes
    register_routes(app,db,bcrypt)
    migrate=Migrate(app,db)

    return app