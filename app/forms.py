from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo


class RegisterForm(FlaskForm):
    name = StringField("Логин: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100)])
    password2 = PasswordField("Повторите пароль: ", validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField("Войти")

class LoginForm(FlaskForm):
    name = StringField("Логин: ", validators=[DataRequired(), Length(min=3, max=16)])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100)])
    submit = SubmitField("Войти")

class NewTaskForm(FlaskForm):
    title = StringField("Заголовок: ", validators=[DataRequired(), Length(min=3, max=16)])
    description = TextAreaField("Описание: ", validators=[DataRequired(), Length(min=3)])
    tags = SelectMultipleField("Выберите тэги: ", choices=[], coerce=int)
    submit = SubmitField("Добавить заметку")
