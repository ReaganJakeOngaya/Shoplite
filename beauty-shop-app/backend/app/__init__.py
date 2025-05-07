from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)    
    CORS(app)  # Enable CORS for all routes
    
    with app.app_context():
        from . import models, routes
        db.create_all()
        
        from .routes import bp as api_bp
        app.register_blueprint(api_bp)

    
        
    return app