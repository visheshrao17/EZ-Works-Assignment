from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, File, User
from app.utils import generate_secure_url

client_bp = Blueprint('client', __name__)

@client_bp.route('/files', methods=['GET'])
@jwt_required()
def list_files():
    files = File.query.all()
    file_list = [{"id": f.id, "filename": f.filename} for f in files]
    return jsonify({"files": file_list})

@client_bp.route('/download/<int:file_id>', methods=['GET'])
@jwt_required()
def download_file(file_id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if user.role != 'client':
        return jsonify({"message": "Unauthorized"}), 403

    file = File.query.get(file_id)
    if not file:
        return jsonify({"message": "File not found"}), 404

    secure_url = generate_secure_url(file.filename)
    return jsonify({"download-link": secure_url, "message": "success"})

@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    user_id = decode_jwt(token)  # Assuming a decode_jwt utility exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Invalid or expired token"}), 400

    user.verified = True
    db.session.commit()
    return jsonify({"message": "Email verified successfully"}), 200
