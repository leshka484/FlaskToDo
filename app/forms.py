from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms import (
    PasswordField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from app.extensions import Session as db
from app.models import Tag


class RegisterForm(FlaskForm):
    name = StringField("Логин: ", validators=[DataRequired()])
    password = PasswordField(
        "Пароль: ", validators=[DataRequired(), Length(min=4, max=100)]
    )
    password2 = PasswordField(
        "Повторите пароль: ", validators=[EqualTo("password"), DataRequired()]
    )
    submit = SubmitField("Войти")


class LoginForm(FlaskForm):
    name = StringField("Логин: ", validators=[DataRequired(), Length(min=3, max=16)])
    password = PasswordField(
        "Пароль: ", validators=[DataRequired(), Length(min=4, max=100)]
    )
    submit = SubmitField("Войти")


class TaskForm(FlaskForm):
    title = StringField(
        "Заголовок: ", validators=[DataRequired(), Length(min=3, max=16)]
    )
    description = TextAreaField(
        "Описание: ", validators=[DataRequired(), Length(min=3)]
    )
    tags = SelectMultipleField("Выберите теги: ", choices=[], coerce=int)


class NewTaskForm(TaskForm):
    submit = SubmitField("Добавить заметку")


class EditTaskForm(TaskForm):
    submit = SubmitField("Сохранить заметку")


class NewTagForm(FlaskForm):
    name = StringField(
        "Название тега: ", validators=[DataRequired(), Length(min=3, max=16)]
    )
    submit = SubmitField("Добавить тег")

    def validate_name(self, field):
        if db.execute(select(Tag).where(Tag.name == field.data)).scalar_one_or_none():
            raise ValidationError("Тег с таким названием уже существует")
