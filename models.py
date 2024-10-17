from app import db

from flask_login import UserMixin

class Users(db.Model,UserMixin):
    __tablename__ = "users"  # Corrected the spelling from __tabelname__

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)  # Added unique constraint
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"UID : {self.uid} User : \"{self.username}\" , password: \"{self.password}\""

    def get_id(self):
        return self.uid


class Posts(db.Model,UserMixin):
    __tablename__ = "posts"

    pid = db.Column(db.Integer, primary_key=True)  # Primary key for Posts table
    title = db.Column(db.String, nullable=False)  # Title of the post
    content = db.Column(db.Text, nullable=False)  # Content of the post
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)  # Foreign key reference to Users table
    user = db.relationship('Users', backref='posts')
    def __repr__(self):
        return f"Post ID : {self.pid}, Title : \"{self.title}\", User ID : {self.user_id}"
