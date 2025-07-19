from app import db
from datetime import datetime
import uuid

class Resume(db.Model):
    __tablename__ = 'resume'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    summary = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(36))
    modified_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    modified_by = db.Column(db.String(36))
    
    # Relationships
    educations = db.relationship('Education', backref='resume', lazy=True, cascade='all, delete-orphan')
    certificates = db.relationship('Certificate', backref='resume', lazy=True, cascade='all, delete-orphan')
    languages = db.relationship('LanguageSkill', backref='resume', lazy=True, cascade='all, delete-orphan')
    domains = db.relationship('Domain', backref='resume', lazy=True, cascade='all, delete-orphan')
    projects = db.relationship('Project', backref='resume', lazy=True, cascade='all, delete-orphan')
    professional_skills = db.relationship('ProfessionalSkill', backref='resume', lazy=True, cascade='all, delete-orphan')

class Education(db.Model):
    __tablename__ = 'education'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = db.Column(db.String(36), db.ForeignKey('resume.id'), nullable=False)
    school = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime)
    grade = db.Column(db.String(20))
    complete_degree = db.Column(db.Boolean, default=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(36))
    modified_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    modified_by = db.Column(db.String(36))

class Certificate(db.Model):
    __tablename__ = 'certificates'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = db.Column(db.String(36), db.ForeignKey('resume.id'), nullable=False)
    certificate = db.Column(db.String(200), nullable=False)
    certificate_authority = db.Column(db.String(200))
    not_expired = db.Column(db.Boolean, default=True)
    issue_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)
    score = db.Column(db.String(20))
    license_no = db.Column(db.String(100))
    certificate_url = db.Column(db.String(500))
    foreign_language = db.Column(db.String(50))
    subject = db.Column(db.String(200))
    is_ctc_sponsor = db.Column(db.Boolean, default=False)
    grade = db.Column(db.String(20))
    certificate_catalog_id = db.Column(db.String(36))
    provider_id = db.Column(db.String(36))
    provider = db.Column(db.String(200))
    field_id = db.Column(db.String(36))
    field = db.Column(db.String(200))
    sub_field_id = db.Column(db.String(36))
    sub_field = db.Column(db.String(200))
    level_id = db.Column(db.String(36))
    level = db.Column(db.String(100))
    status = db.Column(db.Integer, default=0)
    attendance = db.Column(db.Boolean, default=True)
    file_name = db.Column(db.String(255))
    is_synced = db.Column(db.Boolean, default=False)
    is_education = db.Column(db.Boolean, default=False)
    tech_type = db.Column(db.String(100))
    reject_reason = db.Column(db.String(500))
    is_not_has_license_number = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(36))
    modified_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    modified_by = db.Column(db.String(36))

class Language(db.Model):
    __tablename__ = 'languages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(36))
    modified_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    modified_by = db.Column(db.String(36))

class LanguageSkill(db.Model):
    __tablename__ = 'language_skills'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = db.Column(db.String(36), db.ForeignKey('resume.id'), nullable=False)
    language_id = db.Column(db.String(36), db.ForeignKey('languages.id'), nullable=False)
    proficiency = db.Column(db.Integer, default=0)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(36))
    modified_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    modified_by = db.Column(db.String(36))
    
    language = db.relationship('Language', backref='skills')

class Domain(db.Model):
    __tablename__ = 'domains'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = db.Column(db.String(36), db.ForeignKey('resume.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, default=0)
    month = db.Column(db.Integer, default=0)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(36))
    modified_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    modified_by = db.Column(db.String(36))

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = db.Column(db.String(36), db.ForeignKey('resume.id'), nullable=False)
    resume_project_id = db.Column(db.String(36))
    project_id = db.Column(db.String(36))
    name = db.Column(db.String(200), nullable=False)
    project_key = db.Column(db.String(100))
    project_code = db.Column(db.String(100))
    project_rank = db.Column(db.String(10))
    project_lead = db.Column(db.String(200))
    project_category = db.Column(db.String(100))
    customer_code = db.Column(db.String(100))
    contract_type = db.Column(db.String(50))
    url = db.Column(db.String(500))
    company = db.Column(db.String(200))
    type = db.Column(db.String(50))
    team_size = db.Column(db.Integer, default=0)
    search_skill = db.Column(db.Integer, default=0)
    technology = db.Column(db.JSON)
    project_description = db.Column(db.Text)
    groupname = db.Column(db.String(200))
    status = db.Column(db.String(50))
    domain = db.Column(db.String(200))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    pain_points = db.Column(db.Text)
    key_findings = db.Column(db.Text)
    working_process = db.Column(db.Text)
    responsibility = db.Column(db.Text)
    technology_by_pm = db.Column(db.String(500))
    description_by_pm = db.Column(db.Text)
    is_update_team = db.Column(db.Boolean, default=False)
    apply_incompleted = db.Column(db.Boolean, default=False)
    skill = db.Column(db.String(200))
    skill_code = db.Column(db.String(100))
    seniority = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(36))
    modified_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    modified_by = db.Column(db.String(36))

class ProfessionalSkill(db.Model):
    __tablename__ = 'professional_skills'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = db.Column(db.String(36), db.ForeignKey('resume.id'), nullable=False)
    job_title_name = db.Column(db.String(200), nullable=False)
    experience_month = db.Column(db.Integer, default=0)
    experience_year = db.Column(db.Integer, default=0)
    job_fill_by_user = db.Column(db.String(200))
    is_main_skill = db.Column(db.Boolean, default=False)
    project_info = db.Column(db.JSON)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(36))
    modified_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    modified_by = db.Column(db.String(36))
