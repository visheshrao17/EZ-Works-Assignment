from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from app.routes.ops_routes import ops_bp
        from app.routes.client_routes import client_bp
        from app.routes.auth_routes import auth_bp

        app.register_blueprint(ops_bp, url_prefix="/api/ops")
        app.register_blueprint(client_bp, url_prefix="/api/client")
        app.register_blueprint(auth_bp, url_prefix="/api/auth")

        db.create_all()
    return app
