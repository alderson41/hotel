from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room


db = SQLAlchemy()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")


    from .user import routes as user_routes
    from .admin import routes as admin_routes
    from .cook import routes as cook_routes


    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    app.register_blueprint(user_routes.user)
    app.register_blueprint(admin_routes.adminbp)
    app.register_blueprint(cook_routes.cookbp)


    with app.app_context():
        db.create_all()
    return app