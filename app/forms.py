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
    name = StringField(
        "Логин: ",
        validators=[
            DataRequired(),
            Length(
                min=3, max=100, message="Логин может быть длиной от 3 до 100 символов"
            ),
        ],
    )
    password = PasswordField(
        "Пароль: ",
        validators=[
            DataRequired(),
            Length(
                min=4, max=100, message="Пароль может быть длиной от 4 до 100 символов"
            ),
        ],
    )
    password2 = PasswordField(
        "Повторите пароль: ",
        validators=[EqualTo("password", message="Пароли не совпадают"), DataRequired()],
    )
    submit = SubmitField("Войти")


class LoginForm(FlaskForm):
    name = StringField(
        "Логин: ",
        validators=[
            DataRequired(),
            Length(
                min=3, max=100, message="Логин может быть длиной от 3 до 100 символов"
            ),
        ],
    )
    password = PasswordField(
        "Пароль: ",
        validators=[
            DataRequired(),
            Length(
                min=4, max=100, message="Пароль может быть длиной от 4 до 100 символов"
            ),
        ],
    )
    general_errors: set[str] = set()
    submit = SubmitField("Войти")


class TaskForm(FlaskForm):
    title = StringField(
        "Заголовок: ",
        validators=[
            DataRequired(),
            Length(
                min=3, max=30, message="Заголовок может быть длиной от 3 до 30 символов"
            ),
        ],
    )
    description = TextAreaField(
        "Описание: ",
        validators=[
            DataRequired(),
            Length(min=3, message="Описание не может быть короче 3 символов"),
        ],
    )
    tags = SelectMultipleField("Выберите теги: ", choices=[], coerce=int)


class NewTaskForm(TaskForm):
    submit = SubmitField("Добавить заметку")


class EditTaskForm(TaskForm):
    submit = SubmitField("Сохранить заметку")


class NewTagForm(FlaskForm):
    name = StringField(
        "Название тега: ",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=16,
                message="Название тега может быть длиной от 3 до 16 символов",
            ),
        ],
    )
    submit = SubmitField("Добавить тег")

    def validate_name(self, field):
        if db.execute(select(Tag).where(Tag.name == field.data)).scalar_one_or_none():
            raise ValidationError("Тег с таким названием уже существует")
