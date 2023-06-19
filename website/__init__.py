from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin

app = Flask(__name__)
DB_NAME = "database.db"
db = SQLAlchemy()
migrate = Migrate(app, db)


def create_app():
    app.config['SECRET_KEY'] = "0929653ee74200d1322c11721a9e5f27af2d35901a38c0c1f4a7319cde1d8234"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    PROFILE_PICTURE_FOLDER = "./website/static/images/profile_pictures/"
    app.config['PROFILE_PICTURE_FOLDER'] = PROFILE_PICTURE_FOLDER
    from .views import views
    from .auth import auth
    from .models import User, Task, FinishedTask, Comment, UserView, TaskView, CommentView, Event ,EventView
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    admin = Admin(app, name="ProTask")
    admin.add_view(UserView(User, db.session))
    admin.add_view(TaskView(Task, db.session))
    admin.add_view(CommentView(Comment, db.session))
    admin.add_view(EventView(Event, db.session))
    with app.app_context():
        db.init_app(app)
        db.create_all()
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app
