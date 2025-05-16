from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Task, Tag
from app.extensions import Session
from app.crud import *
from app.forms import NewTaskForm

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks")
@login_required
def tasks():
    return render_template("tasks.html")

@tasks_bp.route("/new_task", methods=["GET", "POST"])
@login_required
def new_task():
    form = NewTaskForm()
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]

    if form.validate_on_submit():   
        title = form.title.data
        description = form.description.data
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        create_task(
            db=Session,
            title=title,
            description=description,
            tags=selected_tags
            )
        return redirect(url_for("tasks.tasks"))
    else:
        return render_template("new_task.html", form=form)

