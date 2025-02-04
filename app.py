from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta


# Configration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

#Schelduler Setup
scheduler = BackgroundScheduler()
scheduler.start()

#Task Remender Function
def set_task_reminder(task_id):
    task = Task.query.get(task_id)
    if task and not task.completed:
        print(f"⏰ Reminder: '{task.title}' is due soon!")

#Daily Summery
def daily_summery():
    today = datetime.now().strftime("%Y-%m-%d")
    tasks = Task.query.filter(Task.due_date.like(f"{today}"), Task.completed==False).all()
    if tasks:
        print("📋 Daily Summary:")
        for task in tasks:
            print(f"- {task.title} (Due: {task.due_date})")
    else:
        print("✅ All tasks for today are completed!")


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

        #scheduler remendir if due date/Time is set
            if new_task.due_date:
                due_datetime = datetime.strptime(new_task.due_date,"%Y-%m-%d %H:%M")
                reminder_time = due_datetime - timedelta(minutes=1)
                if reminder_time > datetime.now():
                    scheduler.add_job(set_task_reminder,'date',run_date=reminder_time,args=[new_task.id])
            
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
