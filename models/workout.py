from datetime import datetime, timezone
from models import db

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Float, nullable=False)

    # Relationship to Exercises 
    exercises = db.relationship('Exercise', backref='workout', lazy=True)

    def __repr__(self):
        return f"<Workout {self.id} by User {self.user_id} on {self.date}>"
