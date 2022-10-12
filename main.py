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
list_id = 0

@app.route("/", methods=["GET", "POST"])
def home():
    global list_id
    form = ToDoListForm()
    if form.validate_on_submit():
        sub_objectives = [[obj, False] for obj in form.sub_objectives.data.split(",,") if obj.strip()]
        to_do_list = {
            "id": list_id,
            "title": form.title.data,
            "img_url": form.image_url.data,
            "sub_objectives": sub_objectives,
            "progress": 0,
        }
        data.append(to_do_list)
        list_id += 1
    return render_template("index.html", form=form, data=data)

@app.route("/update/<list_num>/<obj_num>/<current>")
def update_list(list_num: int, obj_num: int, current):
    """Updates the list when an item is checked or unchecked.
    The corresponding button on the webpage is updated as is the progress bar.

    Keyword Arguments:
    list_num -- The index number list that had an objective changed
    obj_num -- The number of the objective in the list. Flask starts at 1 for index so this number needs -1 for true index
    current -- The current state of the objective.
    """
    current_list = data[int(list_num)]
    obj = current_list['sub_objectives']
    # Flask is weird and even trying to force current into bool using function it doesnt work... just check string instead
    if current == "True":
        new_bool = False
    else:
        new_bool = True
    obj[int(obj_num)-1][1] = new_bool
    current_list['progress'] = progress_count(obj)
    return redirect(url_for("home"))

def progress_count(obj_list):
    """Given an objective list calculate the progress of the to do list

    Keyword Arguments:
    obj_list -- the objective list

    Returns an integer between 0 and 100 that denotes the list progress.
    """
    total_items = len(obj_list)
    checked_off = 0
    for obj in obj_list:
        if obj[1]:
            checked_off += 1
    return int((checked_off/total_items)*100)

if __name__ == "__main__":
    app.run(debug=True)