from flask import request
from flask_restx import Namespace, Resource, fields
from app import db
from app.models import Language, LanguageSkill

ns = Namespace('languages', description='Language operations')

# Model definitions for Swagger
language_model = ns.model('Language', {
    'id': fields.String(required=False, description='Language ID'),
    'name': fields.String(required=True, description='Language name'),
    'created_on': fields.DateTime(required=False, description='Created date'),
    'created_by': fields.String(required=False, description='Created by'),
    'modified_on': fields.DateTime(required=False, description='Modified date'),
    'modified_by': fields.String(required=False, description='Modified by')
})

language_skill_model = ns.model('LanguageSkill', {
    'id': fields.String(required=False, description='Language skill ID'),
    'resume_id': fields.String(required=True, description='Resume ID'),
    'language_id': fields.String(required=True, description='Language ID'),
    'proficiency': fields.Integer(required=False, description='Proficiency level'),
    'created_on': fields.DateTime(required=False, description='Created date'),
    'created_by': fields.String(required=False, description='Created by'),
    'modified_on': fields.DateTime(required=False, description='Modified date'),
    'modified_by': fields.String(required=False, description='Modified by'),
    'language': fields.Nested(language_model, required=False)
})

@ns.route('/')
class LanguageList(Resource):
    @ns.marshal_list_with(language_model)
    def get(self):
        """Get all languages"""
        languages = Language.query.all()
        return languages
    
    @ns.expect(language_model)
    @ns.marshal_with(language_model, code=201)
    def post(self):
        """Create a new language"""
        data = request.json
        language = Language(
            name=data['name'],
            created_by=data.get('created_by'),
            modified_by=data.get('modified_by')
        )
        db.session.add(language)
        db.session.commit()
        return language, 201

@ns.route('/<string:language_id>')
class LanguageDetail(Resource):
    @ns.marshal_with(language_model)
    def get(self, language_id):
        """Get a specific language"""
        language = Language.query.get_or_404(language_id)
        return language
    
    @ns.expect(language_model)
    @ns.marshal_with(language_model)
    def put(self, language_id):
        """Update a specific language"""
        language = Language.query.get_or_404(language_id)
        data = request.json
        
        language.name = data.get('name', language.name)
        language.modified_by = data.get('modified_by')
        
        db.session.commit()
        return language
    
    def delete(self, language_id):
        """Delete a specific language"""
        language = Language.query.get_or_404(language_id)
        db.session.delete(language)
        db.session.commit()
        return {'message': 'Language deleted successfully'}, 204

@ns.route('/skills')
class LanguageSkillList(Resource):
    @ns.marshal_list_with(language_skill_model)
    def get(self):
        """Get all language skills"""
        language_skills = LanguageSkill.query.all()
        return language_skills
    
    @ns.expect(language_skill_model)
    @ns.marshal_with(language_skill_model, code=201)
    def post(self):
        """Create a new language skill"""
        data = request.json
        language_skill = LanguageSkill(
            resume_id=data['resume_id'],
            language_id=data['language_id'],
            proficiency=data.get('proficiency', 0),
            created_by=data.get('created_by'),
            modified_by=data.get('modified_by')
        )
        db.session.add(language_skill)
        db.session.commit()
        return language_skill, 201

@ns.route('/skills/<string:skill_id>')
class LanguageSkillDetail(Resource):
    @ns.marshal_with(language_skill_model)
    def get(self, skill_id):
        """Get a specific language skill"""
        language_skill = LanguageSkill.query.get_or_404(skill_id)
        return language_skill
    
    @ns.expect(language_skill_model)
    @ns.marshal_with(language_skill_model)
    def put(self, skill_id):
        """Update a specific language skill"""
        language_skill = LanguageSkill.query.get_or_404(skill_id)
        data = request.json
        
        language_skill.resume_id = data.get('resume_id', language_skill.resume_id)
        language_skill.language_id = data.get('language_id', language_skill.language_id)
        language_skill.proficiency = data.get('proficiency', language_skill.proficiency)
        language_skill.modified_by = data.get('modified_by')
        
        db.session.commit()
        return language_skill
    
    def delete(self, skill_id):
        """Delete a specific language skill"""
        language_skill = LanguageSkill.query.get_or_404(skill_id)
        db.session.delete(language_skill)
        db.session.commit()
        return {'message': 'Language skill deleted successfully'}, 204

@ns.route('/skills/resume/<string:resume_id>')
class LanguageSkillByResume(Resource):
    @ns.marshal_list_with(language_skill_model)
    def get(self, resume_id):
        """Get all language skills for a specific resume"""
        language_skills = LanguageSkill.query.filter_by(resume_id=resume_id).all()
        return language_skills
