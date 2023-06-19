from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from .models import User, Task,  FinishedTask, Comment, Event
from datetime import datetime
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from website import app

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route('/register')
def register():
    return render_template("register.html")


@views.route('/login')
def login():
    return render_template('login.html')


@views.route("/dashboard")
@login_required
def dashboard():
    tasks = Task.query.all()
    user = User.query.all()
    finished = FinishedTask.query.all()
    picture = current_user.picture
    tasks_length = len(tasks)
    if tasks_length == 0:
        redirect(url_for('views.dashboard', picture=picture))
    else:
        tasks = Task.query.all()
        user = User.query.all()
        finished = FinishedTask.query.all()
        picture = current_user.picture
        finished_task_length = len(finished)
        alltasks = tasks_length+finished_task_length
        task_percent = int((tasks_length/alltasks)*100)
        finished_percent = int((finished_task_length/alltasks)*100)
        return render_template("dashboard.html", user=user, alltasks=alltasks, tasks=tasks, finished=finished, picture=picture, task_percent=task_percent, finished_percent=finished_percent)
    return render_template("dashboard.html", user=user, tasks=tasks, finished=finished, picture=picture)


@views.route("/profile/<id>", methods=["POST", "GET"])
@login_required
def profile(id):
    profile = User.query.get_or_404(id)
    if request.method == "POST" and current_user:
        profile.username = request.form.get('username')
        profile.first_name = request.form.get('first_name')
        profile.last_name = request.form.get('last_name')
        profile.id = profile.id
        profile.job = request.form.get('job')
        if profile.job == None:
            profile.job = ""
        profile.email = request.form.get('email')
        profile.password = generate_password_hash(
            request.form.get('password'), method="sha256")
        picture = request.files['picture']
        name = secure_filename(picture.filename)
        picture_name = str(uuid.uuid1())+"_"+name
        saved_file = request.files['picture']
        profile.picture = picture_name
        db.session.commit()
        saved_file.save(os.path.join(
            app.config['PROFILE_PICTURE_FOLDER'], picture_name))
        return redirect(url_for('views.profile', user=current_user, id=current_user.id))
    return render_template("profile.html", user=current_user, id=current_user.id)


@views.route("/projects", methods=["GET", "POST"])
@login_required
def project():
    return render_template("projects.html", user=current_user)


@views.route('/tasks', methods=["POST", "GET"])
@login_required
def tasks():
    task = Task.query

    if current_user and request.method == "POST":
        task.open_task = request.form.get("task")
        task.task_descriptif = request.form.get("task_descriptif")
        tasks = Task(open_task=task.open_task, ongoing_task=task.open_task,
                     operator=current_user.id, task_descriptif=task.task_descriptif)
        db.session.add(tasks)
        db.session.commit()
        return redirect('/description/<task_id>"')
    return render_template("tasks.html", user=current_user, tasks=task)


@views.route('/finished/<id>', methods=['POST', "GET"])
@login_required
def finished(id):
    task = Task.query.filter_by(id=id).first()
    finished = FinishedTask.query.filter_by(id=id).first()
    finishedt = FinishedTask(finished_task=task.open_task,
                             finished_task_operator=task.operator, operator_username=task.user.username)
    db.session.add(finishedt)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("views.dashboard", task=task, finishedt=finished, user=current_user))


@views.route('/update/<id>', methods=["POST", "GET"])
@ login_required
def update(id):
    task = Task.query.get(id)
    if current_user and request.method == "POST":
        task.open_task = request.form["task_to_update"]
        task.ongoing_task = request.form['task_to_update']
        task.task_descriptif = request.form['task_descriptif_to_update']
        db.session.commit()
    return render_template("update.html", task=task, user=current_user)


@views.route('/delete/<id>', methods=["POST", "GET"])
@ login_required
def delete(id):
    task = Task.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("views.dashboard", task=task, user=current_user))


@views.route('/delete_descriptif/<task_descriptif>', methods=["POST", "GET"])
@login_required
def delete_descriptif(task_descriptif):
    task = Task.query.filter_by(task_descriptif=task_descriptif).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully.")
    else:
        flash("Task not found.")

    return redirect(url_for('views.dashboard'))


@views.route("/projects/<username>")
@login_required
def projects(username):
    user = User.query.filter_by(username=username).first()
    task = user.task
    finishedtasks = FinishedTask.query.filter_by(
        finished_task_operator=current_user.id).all()
    return render_template("projects.html", user=current_user, task=task, finishedtasks=finishedtasks, username=username)


@views.route("/description/<task_id>", methods=["POST", "GET"])
@login_required
def description(task_id):
    tasks = Task.query.all()
    task = Task.query.filter_by(id=task_id).first()
    text_comment = request.form.get('comment')
    if text_comment is not None:
        comment = Comment(comment=text_comment,
                          operator=current_user.id, task_id=task_id)
        db.session.add(comment)
        db.session.commit()
    comments = Comment.query.all()

    return render_template("description.html", user=current_user, tasks=tasks, task=task,  comments=comments)


@views.route("/update_comment/<comment_id>", methods=["GET", "POST"])
@login_required
def update_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        flash("comment does not exist")

    if comment.operator != current_user.id:
        flash("yout not allowed to modify this Comment")
    if request.method == "POST":
        new_comment = request.form.get("comment")
        comment.comment = new_comment
        db.session.commit()
        flash("Comment updated successfully.")
        return redirect(url_for("views.description", task_id=comment.task_id))
    return render_template("update_comment.html", task_id=comment.task_id)


@ views.route("/delete_comment/<comment_id>", methods=["GET", "POST"])
@ login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment.operator != current_user.id:
        flash("Comment was not deleted")

    if request.method == "POST":
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted successfully.")
        return redirect(url_for("views.description", task_id=comment.task_id))
    return render_template("description.html", task_id=comment.task_id, user=current_user)


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")


@ views.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@ views.route("/search_result", methods=["POST"])
@ login_required
def search_result():
    form = SearchForm()
    task = Task.query
    output_searched = form.searched.data
    search_result = task.filter(Task.open_task.like('%'+output_searched+"%"))
    search_result = search_result.order_by(Task.open_task).all()
    return render_template("search_result.html", user=current_user, output=output_searched, form=form, search_result=search_result)


@ views.route("/calendar")
@ login_required
def calendar():
    task = Task.query
    events = Event.query.all()
    return render_template("calendar.html", user=current_user, events=events, task=task)


@app.route('/calendar/add-event', methods=['GET', 'POST'])
def add_event():
    users = User.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        start_str = request.form.get('start')
        end_str = request.form.get('end')
        url = request.form.get('url')

        if start_str:
            start = datetime.strptime(start_str, '%Y-%m-%d')
        else:
            start = None

        if end_str:
            end = datetime.strptime(end_str, '%Y-%m-%d')
        else:
            end = start

        event = Event(title=title, start=start, end=end, url=url)
        db.session.add(event)
        db.session.commit()
        flash('Event added successfully', category='success')
        return redirect(url_for('views.calendar'))

    return render_template('add_event.html', user=current_user, users=users)


@ app.errorhandler(404)
def error(e):
    return render_template("404.html"), 404


@ app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500
