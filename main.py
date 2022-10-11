import os

from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager

from forms import ToDoListForm, ObjectiveForm
from model import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///to-do-list.db"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
db.init_app(app)
data = []

@app.route("/", methods=["GET", "POST"])
def home():
    form = ToDoListForm()
    if form.validate_on_submit():
        sub_objectives = [[obj, ObjectiveForm()] for obj in form.sub_objectives.data.split(",,")]
        to_do_list = {
            "Title": form.title.data,
            "img_url": form.image_url.data,
            "Sub_Objectives": sub_objectives,
            "progress": 0,
        }
        data.append(to_do_list)
    return render_template("index.html", form=form, data=data)

if __name__ == "__main__":
    app.run(debug=True)