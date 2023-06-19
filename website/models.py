from . import db
from flask_login import UserMixin, current_user
from sqlalchemy.sql import func
from flask import abort
from flask_admin.contrib.sqla import ModelView


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    job = db.Column(db.String(20))
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    picture = db.Column(db.String())
    task = db.relationship('Task', backref='user', passive_deletes=True)
    comment = db.relationship('Comment', backref='user', passive_deletes=True)

    def __repr__(self):
        return '<User %r>' % (self.username)


class UserView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "admin":
            return True
        else:
            abort(404)
    form_columns = ['username', 'email', 'date_created']
    column_exclude_list = ['password']
    can_create = False
    can_edit = False
    can_view_details = True


class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    open_task = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    ongoing_task = db.Column(db.String(20), nullable=True)

    task_descriptif = db.Column(db.String(200), nullable=False)
    username = db.relationship(
        'User', backref="user",  passive_deletes=True, overlaps="posts,user")
    operator = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    finished = db.relationship(
        "FinishedTask", backref="task", passive_deletes=True)
    comment = db.relationship('Comment', backref='task', passive_deletes=True)

    def __repr__(self):
        return "<Task%r>" % (self.id)


class TaskView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "admin":
            return True
        else:
            abort(404)
    form_columns = ['open_task', "ongoing_task", 'username', 'date_created']


class FinishedTask(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    finished_task = db.Column(db.String(20), nullable=False)

    operator_username = db.Column(db.String(20), nullable=False)
    finished_task_operator = db.Column(db.Integer, db.ForeignKey(
        "task.id", ondelete="CASCADE"))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             default=func.now(), nullable=False)
    operator = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"))
    task_id = db.Column(db.Integer, db.ForeignKey(
        'task.id', ondelete="CASCADE"))
    username = db.relationship(
        'User', backref="auth", passive_deletes=True, overlaps="comment,user")

    def __repr__(self):
        return '<Comment %r>' % (self.id)


class CommentView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "admin":
            return True
        else:
            abort(404)
    form_columns = ['comment', 'date_created', "username"]
    can_create = False
    can_view_details = True


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start = db.Column(db.DateTime(timezone=True))
    end = db.Column(db.DateTime(timezone=True))
    url = db.Column(db.String(200))


class EventView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "admin":
            return True
        else:
            abort(404)
    form_columns = ['title', 'start', "end"]
    column_searchable_list = ['title']
    column_filters = ['start', 'end']
