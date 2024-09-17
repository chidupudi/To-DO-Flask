from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/todo_db"
mongo = PyMongo(app)
# Get the tasks collection
tasks_collection = mongo.db.tasks
@app.route('/')
def index():
    tasks = tasks_collection.find()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    if title:
        tasks_collection.insert_one({"title": title, "done":  False})
    return redirect(url_for('index'))

@app.route('/toggle/<task_id>')
def toggle_task(task_id):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"done": not task['done']}})
    return redirect(url_for('index'))

@app.route('/delete/<task_id>')
def delete_task(task_id):
    tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
