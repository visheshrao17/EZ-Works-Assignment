from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import hashlib
import hmac

SECRET_KEY = "your_secret_key"

def hash_password(password):
    return generate_password_hash(password)

def check_password(password, hashed):
    return check_password_hash(hashed, password)

def generate_jwt(user_id):
    return create_access_token(identity=user_id)

def generate_secure_url(filename):
    signature = hmac.new(SECRET_KEY.encode(), filename.encode(), hashlib.sha256).hexdigest()
    return f"/download/{filename}?sig={signature}"
