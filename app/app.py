from flask import Flask
from app.routes.auth import auth_bp
from app.extensions import Session, login_manager
from app.models import User
from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv(dotenv_path=Path(__file__).parent / ".env")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.register_blueprint(auth_bp) # Регистрация шаблона аунтефикаций

login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()
    
if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def index():
    return "Hello World!"

#flask run --port=8000
