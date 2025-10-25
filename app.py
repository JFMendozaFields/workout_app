from flask import Flask
from models import db
from models.user import User
from routes import register_routes


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



# Pull in Registered Routes
register_routes(app)

@app.route('/')
def home():
    return "Workout App is running!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

