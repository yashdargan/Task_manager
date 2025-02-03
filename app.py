from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Configration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

#intitalize db
db = SQLAlchemy(app)

#Writing schema
class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(250))
    due_date = db.Column(db.String(10))
    completed = db.Column(db.Boolean,default=False)

#Database creation
with app.app_context():
    db.create_all()

#home API route
@app.route('/')
def home():
    return jsonify({'message':'Working it Home page!!!'})

#Task API route
@app.route('/task',methods=['GET','POST'])
def tasks_list():
    #Get All Task(GET)
    if request.method == 'GET':
        tasks = Task.query.all()
        result = [{'id':task.id,'title':task.title,'description':task.description,'due_date':task.due_date,'completed':task.completed}
                   for task in tasks
                 ]
        return jsonify(result)
    #Post all Task(POST)
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
#Task API route - Specific operation(PUT,DELETE)
@app.route('/task/<int:task_id>',methods=['PUT','DELETE'])
def task_edition(task_id):
    task = Task.query.get_or_404(task_id)
    #Update Task
    if request.method == 'PUT':
        data = request.get_json()
        if data:
            task.title = data.get('title',task.title)
            task.description = data.get('description',task.description)
            task.due_date = data.get('due_date',task.due_date)
            task.completed = data.get('completed',task.completed)
            db.session.commit()
            return jsonify({'message':'Task Updated Successfully!!!'})
    #Deleted Task
    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message':'Task Deleted Successfully'})


if __name__ == "__main__":
    app.run(debug=True)
