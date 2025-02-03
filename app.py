from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(250))
    due_date = db.Column(db.String(10))
    completed = db.Column(db.Boolean,default=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return jsonify({'message':'Working it Home page!!!'})

@app.route('/task',methods=['GET','POST'])
def tasks_list():
    if request.method == 'GET':
        tasks = Task.query.all()
        result = [{'id':task.id,'title':task.title,'description':task.description,'due_date':task.due_date,'completed':task.completed}
                   for task in tasks
                 ]
        return jsonify(result)
    if request.method == 'POST':
        data = request.get_json()
        if data:
            new_task = Task(
            title = data['title'],
            description = data.get('description',''),
            due_date = data.get('due_date',None),
            )
            db.session.add(new_task)
            db.session.commit()
            return jsonify({'message':'Task Added Suceesfully!!!'}),201

if __name__ == "__main__":
    app.run(debug=True)
