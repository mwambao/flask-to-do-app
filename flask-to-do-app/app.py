
from enum import unique
import os


from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy

project_directory = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(project_directory, "tasks.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_file

db = SQLAlchemy(app)


class Tasks(db.Model):
    task = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    status = db.Column(db.String(80))

 #   def __repr__(self):
 #     return "<Task: {}>".format(self.task)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        task = Tasks(task=request.form.get("task"))
        status = Tasks(status=request.form.get("status"))

        db.session.add(task,status)
        db.session.commit()

    tasks = Tasks.query.all()
    return render_template("home.html", tasks=tasks)



if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)