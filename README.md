
# FlaskToDo — To-Do веб-приложение на Flask

**FlaskToDo** — это простое, но функциональное веб-приложение для управления личными задачами. Пользователи могут регистрироваться, входить в аккаунт и управлять своими задачами в индивидуальном списке.

## Функциональность

- Регистрация и авторизация пользователей
- Создание, редактирование и удаление задач
- Хранение задач отдельно для каждого пользователя
- Ограничение доступа к задачам только после входа
- Тестирование бизнес-логики с использованием Pytest

## Стек технологий

- **Язык программирования**: Python
- **Фреймворк**: Flask
- **База данных**: PostgreSQL
- **ORM**: SQLAlchemy
- **Тестирование**: Pytest
- **Frontend**: HTML, CSS

## Установка и запуск проекта

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/leshka484/FlaskToDo.git
   cd FlaskToDo
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Добавьте файл .env c содержимым:
   ```
    POSTGRES_USER=# Имя пользователя PostgreSQL
    POSTGRES_PASSWORD=# Пароль PostgresSQL
    POSTGRES_HOST=localhost
    POSTGRES_DB=# Название БД
    SECRET_KEY=# Секретный ключ для Flask приложения(пример: 9f2b1c7d4358adcb98be871fa3472f1d8fc12c88a4bb7630c7e4d4ab7f3cf456)
    ```
5. Инициализируйте базу данных:
   ```bash
   alembic upgrade head
   ```

6. Запустите сервер:
   ```bash
   cd app 
   flask run
   ```

7. Откройте в браузере:
   ```
   http://127.0.0.1:5000/
   ```

## Структура проекта

- `app/` — основное приложение Flask (routes, models, forms)
- `templates/` — HTML-шаблоны
- `static/` — CSS/JS файлы
- `tests/` — модульные тесты на Pytest
