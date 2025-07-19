from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for all domains on all routes
    CORS(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize Flask-RESTX
    api = Api(app, 
              version='1.0', 
              title='Interview Co-Pilot API',
              description='API for managing interview projects and resumes',
              doc='/swagger/')
    
    # Import models to ensure they are registered with SQLAlchemy
    from app import models
    
    # Register namespaces
    from app.routes.resume_routes import ns as resume_ns
    from app.routes.education_routes import ns as education_ns
    from app.routes.certificate_routes import ns as certificate_ns
    from app.routes.language_routes import ns as language_ns
    from app.routes.domain_routes import ns as domain_ns
    from app.routes.project_routes import ns as project_ns
    from app.routes.professional_skill_routes import ns as professional_skill_ns
    
    api.add_namespace(resume_ns)
    api.add_namespace(education_ns)
    api.add_namespace(certificate_ns)
    api.add_namespace(language_ns)
    api.add_namespace(domain_ns)
    api.add_namespace(project_ns)
    api.add_namespace(professional_skill_ns)
    
    return app
