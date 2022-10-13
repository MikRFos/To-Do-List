from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL, Optional


class ToDoListForm(FlaskForm):
    title = StringField("List Title", validators=[DataRequired()])
    image_url = StringField("Image URL", validators=[Optional(), URL()])
    sub_objectives = StringField("List Sub-Objectives", render_kw={"placeholder":"Separate with double comma (,,)"},
                                 validators=[DataRequired()])
    submit = SubmitField("Submit")

class ObjectiveForm(FlaskForm):
    check = BooleanField(validators=[Optional()])
    submit = SubmitField("Submit")