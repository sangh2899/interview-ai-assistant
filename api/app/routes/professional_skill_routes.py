from flask import request
from flask_restx import Namespace, Resource, fields
from app import db
from app.models import ProfessionalSkill

ns = Namespace('professional-skills', description='Professional skill operations')

# Model definitions for Swagger
professional_skill_model = ns.model('ProfessionalSkill', {
    'id': fields.String(required=False, description='Professional skill ID'),
    'resume_id': fields.String(required=True, description='Resume ID'),
    'job_title_name': fields.String(required=True, description='Job title or skill name'),
    'experience_month': fields.Integer(required=False, description='Experience in months'),
    'experience_year': fields.Integer(required=False, description='Experience in years'),
    'job_fill_by_user': fields.String(required=False, description='Job filled by user'),
    'is_main_skill': fields.Boolean(required=False, description='Main skill flag'),
    'project_info': fields.List(fields.Raw, required=False, description='Project information'),
    'created_on': fields.DateTime(required=False, description='Created date'),
    'created_by': fields.String(required=False, description='Created by'),
    'modified_on': fields.DateTime(required=False, description='Modified date'),
    'modified_by': fields.String(required=False, description='Modified by')
})

@ns.route('/')
class ProfessionalSkillList(Resource):
    @ns.marshal_list_with(professional_skill_model)
    def get(self):
        """Get all professional skills"""
        professional_skills = ProfessionalSkill.query.all()
        return professional_skills
    
    @ns.expect(professional_skill_model)
    @ns.marshal_with(professional_skill_model, code=201)
    def post(self):
        """Create a new professional skill"""
        data = request.json
        professional_skill = ProfessionalSkill(
            resume_id=data['resume_id'],
            job_title_name=data['job_title_name'],
            experience_month=data.get('experience_month', 0),
            experience_year=data.get('experience_year', 0),
            job_fill_by_user=data.get('job_fill_by_user'),
            is_main_skill=data.get('is_main_skill', False),
            project_info=data.get('project_info'),
            created_by=data.get('created_by'),
            modified_by=data.get('modified_by')
        )
        db.session.add(professional_skill)
        db.session.commit()
        return professional_skill, 201

@ns.route('/<string:skill_id>')
class ProfessionalSkillDetail(Resource):
    @ns.marshal_with(professional_skill_model)
    def get(self, skill_id):
        """Get a specific professional skill"""
        professional_skill = ProfessionalSkill.query.get_or_404(skill_id)
        return professional_skill
    
    @ns.expect(professional_skill_model)
    @ns.marshal_with(professional_skill_model)
    def put(self, skill_id):
        """Update a specific professional skill"""
        professional_skill = ProfessionalSkill.query.get_or_404(skill_id)
        data = request.json
        
        professional_skill.job_title_name = data.get('job_title_name', professional_skill.job_title_name)
        professional_skill.experience_month = data.get('experience_month', professional_skill.experience_month)
        professional_skill.experience_year = data.get('experience_year', professional_skill.experience_year)
        professional_skill.job_fill_by_user = data.get('job_fill_by_user', professional_skill.job_fill_by_user)
        professional_skill.is_main_skill = data.get('is_main_skill', professional_skill.is_main_skill)
        professional_skill.project_info = data.get('project_info', professional_skill.project_info)
        professional_skill.modified_by = data.get('modified_by')
        
        db.session.commit()
        return professional_skill
    
    def delete(self, skill_id):
        """Delete a specific professional skill"""
        professional_skill = ProfessionalSkill.query.get_or_404(skill_id)
        db.session.delete(professional_skill)
        db.session.commit()
        return {'message': 'Professional skill deleted successfully'}, 204

@ns.route('/resume/<string:resume_id>')
class ProfessionalSkillByResume(Resource):
    @ns.marshal_list_with(professional_skill_model)
    def get(self, resume_id):
        """Get all professional skills for a specific resume"""
        professional_skills = ProfessionalSkill.query.filter_by(resume_id=resume_id).all()
        return professional_skills
