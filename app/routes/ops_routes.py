import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, File, User
from werkzeug.utils import secure_filename

ops_bp = Blueprint('ops', __name__)
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {'pptx', 'docx', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ops_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if user.role != 'ops':
        return jsonify({"message": "Unauthorized"}), 403

    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        new_file = File(filename=filename, uploader_id=user.id)
        db.session.add(new_file)
        db.session.commit()
        return jsonify({"message": "File uploaded successfully"}), 201
    return jsonify({"message": "Invalid file type"}), 400
