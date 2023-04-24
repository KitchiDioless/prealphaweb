from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class ProjectsForm(FlaskForm):
    title = StringField('Тема', validators=[DataRequired()])
    content = TextAreaField("Содержание", validators=[DataRequired()])
    teachername = StringField('Имя преподователя', validators=[DataRequired()])
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')