
import os

from flask import Flask, redirect, render_template, request

from flask_sqlalchemy import SQLAlchemy

project_directory = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(project_directory, "tasks.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_file

db = SQLAlchemy(app)


class Tasks(db.Model):
    task = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    status = db.Column(db.String(80))

    def __init__(self, task, status):
        self.task = task
        self.status = status


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        task = Tasks(request.form.get("task"), request.form.get("status"))

        db.session.add(task)
        db.session.commit()

    tasks = Tasks.query.all()
    return render_template("home.html", tasks=tasks)

@app.route("/update", methods=["POST"])
def update():
    newtask = request.form.get("newtask")
    oldtask = request.form.get("oldtask")

    newstatus = request.form.get("newstatus")
    oldstatus = request.form.get("oldstatus")

    task = Tasks.query.filter_by(task=oldtask, status=oldstatus).first()
    task.task = newtask
    task.status = newstatus
    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    task = request.form.get("task")
    task = Tasks.query.filter_by(task=task).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/")


#if __name__=="__main__":
#    app.run(debug=True)