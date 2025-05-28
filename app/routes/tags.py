from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from app.crud import create_tag
from app.extensions import Session
from app.forms import NewTagForm

tags_bp = Blueprint("tags", __name__)


@tags_bp.route("/new_tag", methods=["GET", "POST"])
@login_required
def new_tag():
    form = NewTagForm()
    if form.validate_on_submit():
        name = form.name.data
        create_tag(db=Session, name=name)
        flash("Тег добавлен", "success")
        return redirect(url_for("index"))
    else:
        return render_template("new_tag.html", form=form)
