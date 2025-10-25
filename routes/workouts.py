from flask import Blueprint, jsonify, request
from models.workout import Workout
from models.exercise import Exercise
from datetime import datetime

workouts_bp = Blueprint('workouts', __name__, url_prefix='/workouts')


# Route to view all workouts
@workouts_bp.route('/', methods=['GET'])
def get_all_workouts():
    workouts = Workout.query.all()
    results = []
    for w in workouts:
        results.append({
            'id':w.id,
            'user_id': w.user_id,
            'date': w.date.isoformat(),
            'notes':w.notes,
            'duration': w.duration,
            'exercises': [
                {
                    'id': e.id,
                    'name': e.name,
                    'sets': e.sets,
                    'reps': e.reps,
                    'weight': e.weight
                } for e in w.exercises
            ]
        })
    return jsonify(results), 200

# Route for viewing a specific workout bu ID
@workouts_bp.route('/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    result = {
        'id': workout.id,
        'user_id': workout.user_id,
        'date': workout.date.isoformat(),
        'notes': workout.notes,
        'duration': workout.duration,
        'exercises': [
            {
                'id': e.id,
                'name': e.name,
                'sets': e.sets,
                'reps': e.reps,
                'weight': e.weight
            } for e in workout.exercises
        ]
    }
    return jsonify(result), 200


# Route to add new workouts
@workouts_bp.route('/add', methods=['POST'])
def add_workout():
    data = request.get_json() # GETs JSON data from request body

    # Basic Validation
    if not data:
        return {'error': 'No input data provided'}, 400
    
    user_id = data.get('user_id') # default user for now
    date = data.get('date')
    notes = data.get('notes', '')
    duration = data.get('duration', 0)
    exercises_data = data.get('exercises', [])
    
    if not date or not duration:
        return {'error': 'Date and duration are required'}, 400
    
    #Convert date string to date object
    try:
        date_obj = datetime.fromisoformat(date)
    except ValueError:
        return { 'error': 'Invalid date formatm, use YYYY-MM-DD'}, 400
    
    # Create Workout instance
    workout = Workout(
        user_id=user_id,
        date=date_obj,
        notes=notes,
        duration=duration
    )

    # Add exercises to workout
    for ex in exercises_data:
        exercise = Exercise(
            workout=workout,
            name=ex.get('name'),
            sets=ex.get('sets', 0),
            reps=ex.get('reps', 0),
            weight=ex.get('weight',0)
        ) # SQLALCHEMY relationship handles linking
    
    # Save to database
    from models import db
    db.session.add(workout)
    db.session.commit()

    return {'message': 'Workout added successfully', 'workout_id': workout.id}, 201

