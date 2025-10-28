from flask import Blueprint, request, jsonify
from models import db
from models.user import User 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return {"message": "Missing JSON in request"}, 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')


    if not username or not email or not password:
        return {"message": "Username, email, and password are required"}, 400
    
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return {"message": "User with that username and/or email already exists"}, 400
    
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return {"message": "User registered successfully"}, 201

@auth_bp.route('login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return {"message": "Missing JSON in request"}, 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return {"Message": "Username and password are required"}, 400
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return {"message": "Invalid username or password"}, 401
    
    # Identity payload 
    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token, "user": {"id": user.id, "username": user.username, "email": user.email}}, 200

# Protected test-route
@auth_bp.route('protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {"Logged in as ": current_user}, 200
