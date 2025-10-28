from flask import Flask
from models import db
from models.user import User
from routes import register_routes
from flask_jwt_extended import JWTManager
import os

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'PyrusandPersephone25!!')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600 # 1 hour in seconds


    # Binds Database to Flask App
    db.init_app(app)

    # Initilize JWT Manager
    jwt = JWTManager(app)

    # Pull in Registered Routes
    register_routes(app)


    # Database initialization
    @app.cli.command('init-db')
    def init_db():
        db.create_all()
        print("Database initialized!")
    return app


    @app.route('/')
    def home():
        return "Workout App is running!"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    create_app().run(debug=True)
