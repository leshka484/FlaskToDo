from flask import Flask, render_template
from app.routes.auth import auth_bp
from app.routes.tasks import tasks_bp
from app.extensions import Session, login_manager
from app.models import User
from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.register_blueprint(auth_bp) # Регистрация шаблона аунтефикаций
app.register_blueprint(tasks_bp) # Регистрация шаблона щаметок


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
    return render_template("index.html")

#flask run --port=8000
