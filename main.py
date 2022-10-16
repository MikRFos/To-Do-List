import os

from flask import Flask, render_template, url_for, redirect, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from forms import ToDoListForm, ObjectiveForm, RegistryForm, LoginForm
from model import db, User, List, Objective

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_PATH")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
db.init_app(app)
data = []
list_id = 0

login_manager = LoginManager(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/", methods=["GET", "POST"])
def home():
    global list_id

    if current_user.is_authenticated:
        return redirect("home")

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
        print("list added")
        list_id += 1

    active_lists = [todolist for todolist in data if todolist['progress'] < 100]
    completed_lists = [todolist for todolist in data if todolist['progress'] >= 100]

    return render_template("index.html", form=form, data=data, active=active_lists, completed=completed_lists)

@app.route("/home", methods=["GET", "POST"])
@login_required
def user_home():

    form = ToDoListForm()

    if form.validate_on_submit():
        sub_objectives = [[obj, False] for obj in form.sub_objectives.data.split(",,") if obj.strip()]
        new_list = List(title=form.title.data, img_url=form.image_url.data, progress=0, user_id=current_user.id)
        db.session.add(new_list)
        db.session.commit()
        for obj in sub_objectives:
            new_obj = Objective(list_id=new_list.id, objective_text=obj[0], complete=False)
            db.session.add(new_obj)
        db.session.commit()

    list_data = List.query.filter_by(user_id=current_user.id).all()
    active_lists = [todolist for todolist in list_data if todolist.progress < 100]
    completed_lists = [todolist for todolist in list_data if todolist.progress >= 100]
    return render_template("user_home.html", form=form, data=list_data, active=active_lists, completed=completed_lists)

@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Register a user.
    If successfull also logs user in.
    If unsuccessfull sends a flash message to the webpage to display the error.
    """
    form = RegistryForm()
    if form.validate_on_submit():
        """
        if User.query.filter(func.lower(User.username) == func.lower(form.username.data)).first():
            # User already Exists
            flash("Username Taken")
        else:
        """
        if form.password.data == form.password_confirmation.data:
            hashed_salted_pass = generate_password_hash(form.password.data, salt_length=32)
            new_user = User(username=form.username.data, password=hashed_salted_pass)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

            return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs a user in if correct username/password is entered.
    Sends a flash message to the webpage if the login is unsuccessful
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(func.lower(User.username) == func.lower(form.username.data)).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("user_home"))
            flash("Incorrect Password")
            return redirect(url_for("login"))
        flash("Username Does Not Exist")
        return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/update/<list_num>/<obj_num>/<current>")
def update_list(list_num: int, obj_num: int, current):
    """Updates the list when an item is checked or unchecked.
    The corresponding button on the webpage is updated as is the progress bar.

    Keyword Arguments:
    list_num -- The index number list that had an objective changed
    obj_num -- The number of the objective in the list. Flask starts at 1 for index so this number needs -1 for true index
    current -- The current state of the objective.
    """
    # Flask is weird and even trying to force current into bool using function it doesnt work... just check string instead
    if current == "True":
        new_bool = False
    else:
        new_bool = True
    if current_user.is_authenticated:
        current_list = List.query.get(list_num)
        if new_bool:
            current_list.progress += (100/len(current_list.objectives))
        else:
            current_list.progress -= (100 / len(current_list.objectives))
        current_list.objectives[int(obj_num)-1].complete = new_bool
        db.session.commit()
    else:
        current_list = data[int(list_num)]
        obj = current_list['sub_objectives']
        obj[int(obj_num) - 1][1] = new_bool
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
    return int((checked_off / total_items) * 100)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
