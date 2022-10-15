from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    lists = db.relationship("List", back_populates="user")

class List(db.Model):
    __tablename__ = "lists"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String(250), nullable=True)
    progress = db.Column(db.Integer, nullable=False)
    objectives = db.relationship("Objective", back_populates="list")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="lists")

class Objective(db.Model):
    __tablename__ = "objectives"
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey("lists.id"), nullable=False)
    list = db.relationship("List", back_populates="objectives")
    objective_text = db.Column(db.Text, nullable=False)
    complete = db.Column(db.Boolean, nullable=False)