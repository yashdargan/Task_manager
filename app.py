from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SESSION_DATABASE_URI'] = 'sqlite:///task.db'
app.config['SESSION_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class Task(db.model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(250))
    due_date = db.Column(db.String(10))
    completed = db.Column(db.Boolean,default=False)

with app.app_context():
    db.create_all()



