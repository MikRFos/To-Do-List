from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, URL, Optional, Length


class ToDoListForm(FlaskForm):
    title = StringField("List Title", validators=[DataRequired()])
    image_url = StringField("Image URL", validators=[Optional(), URL()])
    sub_objectives = StringField("List Sub-Objectives", render_kw={"placeholder":"Separate with double comma (,,)"},
                                 validators=[DataRequired()])
    submit = SubmitField("Submit")

class ObjectiveForm(FlaskForm):
    check = BooleanField(validators=[Optional()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Login")


class RegistryForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=5,
                                                              message="Username must be at least 5 characters long")])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=6,
                                                                message="Password must be at least 6 characters long")])
    password_confirmation = PasswordField("Re-Enter Password", validators=[DataRequired(), Length(min=6)])
    register = SubmitField("Register")
