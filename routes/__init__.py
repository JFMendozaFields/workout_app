from routes.workouts import workouts_bp
from routes.auth import auth_bp


def register_routes(app):
    app.register_blueprint(workouts_bp)
    app.register_blueprint(auth_bp)
