from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required
from sqlalchemy import select

from app.crud import create_task, read_task, update_task
from app.crud import delete_task as db_delete_task
from app.extensions import Session
from app.forms import EditTaskForm, NewTaskForm, TaskForm
from app.models import Tag

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/tasks")
@login_required
def tasks():
    return render_template("tasks.html")


@tasks_bp.route("/new_task", methods=["GET", "POST"])
@login_required
def new_task():
    form = NewTaskForm()
    setup_task_form(form)

    if form.validate_on_submit():
        create_task(
            db=Session,
            title=form.title.data,
            description=form.description.data,
            tags=Session.execute(select(Tag).where(Tag.id.in_(form.tags.data)))
            .scalars()
            .all(),
        )
        flash("Заметка добавлена!", "success")
        return redirect(url_for("tasks.tasks"))
    return render_template("task_form.html", form=form, title="Новая заметка")


@tasks_bp.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id: int):
    task = read_task(db=Session, task_id=task_id)
    form = EditTaskForm(obj=task)
    setup_task_form(form)
    if request.method == "GET":
        form.tags.data = [tag.id for tag in task.tags]

    if form.validate_on_submit():
        update_task(
            db=Session,
            task_id=task_id,
            title=form.title.data,
            description=form.description.data,
            tags=list(Session.execute(select(Tag).where(Tag.id.in_(form.tags.data)))
            .scalars()
            .all()),
        )
        flash("Заметка изменена!", "success")
        return redirect(url_for("tasks.tasks"))
    return render_template("task_form.html", form=form, title="Изменить заметку")


def setup_task_form(form: TaskForm):
    form.tags.choices = [
        (tag.id, tag.name) for tag in Session.execute(select(Tag)).scalars().all()
    ]


@tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id: int):
    db_delete_task(Session, task_id=task_id)
    flash("Заметка удалена!", "success")
    return Response(status=204)
