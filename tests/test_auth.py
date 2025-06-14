import pytest
from flask import session
from flask_login import current_user
from sqlalchemy import select

from app.models import User


def test_register(client, db_session):
    assert client.get("/register").status_code == 200
    response = client.post(
        "/register",
        data={"name": "testuser", "password": "testpswrd", "password2": "testpswrd"},
    )
    assert response.headers["Location"] == "/login"
    user = db_session.execute(
        select(User).where(User.name == "testuser")
    ).scalar_one_or_none()
    assert user is not None


def test_login(client, db_session, test_user):
    assert client.get("/login").status_code == 200
    response = client.post(
        "/login",
        data={"name": "testuser", "password": "testpswrd"},
    )
    assert response.headers["Location"] == "/"

    with client:
        client.get("/")
        assert int(session["_user_id"]) == 1
        assert current_user.name == "testuser"


@pytest.mark.parametrize(
    ("name", "password", "password2", "message"),
    (
        ("as", "asda", "asda", "Логин может быть длиной от 3 до 100 символов"),
        ("asd", "asd", "asd", "Пароль может быть длиной от 4 до 100 символов"),
        ("asd", "asda", "asdff", "Пароли не совпадают"),
        (
            "a" * 101,
            "asdf",
            "asdf",
            "Логин может быть длиной от 3 до 100 символов",
        ),
        (
            "asd",
            "a" * 101,
            "a" * 101,
            "Пароль может быть длиной от 4 до 100 символов",
        ),
    ),
)
def test_register_validate_input(client, name, password, password2, message):
    response = client.post(
        "/register",
        data={"name": name, "password": password, "password2": password2},
    )
    assert message in response.get_data(as_text=True)


@pytest.mark.parametrize(
    ("name", "password", "message"),
    (
        ("as", "asda", "Логин может быть длиной от 3 до 100 символов"),
        ("asd", "asd", "Пароль может быть длиной от 4 до 100 символов"),
        (
            "a" * 101,
            "asdf",
            "Логин может быть длиной от 3 до 100 символов",
        ),
        (
            "asd",
            "a" * 101,
            "Пароль может быть длиной от 4 до 100 символов",
        ),
        ("testuser", "Неправильный пароль", "Неверный логин или пароль"),
        ("Неверный логин", "Неправильный пароль", "Неверный логин или пароль"),
        ("Неверный логин", "testpswrd", "Неверный логин или пароль")
    ),
)
def test_login_validate_input(client, name, password, message, test_user):
    response = client.post("/login", data={"name": name, "password": password})
    assert message in response.get_data(as_text=True)
