from flask import Blueprint, request, jsonify
from app.models import db, User
from app.utils import hash_password, check_password, generate_jwt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'client')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = hash_password(password)
    new_user = User(email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    verification_link = f"/api/auth/verify/{generate_jwt(new_user.id)}"
    return jsonify({"message": "Account created", "verification_link": verification_link}), 201
