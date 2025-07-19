from flask import request
from flask_restx import Namespace, Resource, fields
from app import db
from app.models import Education
from datetime import datetime

ns = Namespace('education', description='Education operations')

# Model definitions for Swagger
education_model = ns.model('Education', {
    'id': fields.String(required=False, description='Education ID'),
    'resume_id': fields.String(required=True, description='Resume ID'),
    'school': fields.String(required=True, description='School name'),
    'degree': fields.String(required=True, description='Degree name'),
    'major': fields.String(required=True, description='Major field'),
    'start': fields.DateTime(required=True, description='Start date'),
    'end': fields.DateTime(required=False, description='End date'),
    'grade': fields.String(required=False, description='Grade or GPA'),
    'complete_degree': fields.Boolean(required=False, description='Degree completed'),
    'created_on': fields.DateTime(required=False, description='Created date'),
    'created_by': fields.String(required=False, description='Created by'),
    'modified_on': fields.DateTime(required=False, description='Modified date'),
    'modified_by': fields.String(required=False, description='Modified by')
})

@ns.route('/')
class EducationList(Resource):
    @ns.marshal_list_with(education_model)
    def get(self):
        """Get all education records"""
        education_records = Education.query.all()
        return education_records
    
    @ns.expect(education_model)
    @ns.marshal_with(education_model, code=201)
    def post(self):
        """Create a new education record"""
        data = request.json
        education = Education(
            resume_id=data['resume_id'],
            school=data['school'],
            degree=data['degree'],
            major=data['major'],
            start=datetime.fromisoformat(data['start'].replace('Z', '+00:00')),
            end=datetime.fromisoformat(data['end'].replace('Z', '+00:00')) if data.get('end') else None,
            grade=data.get('grade'),
            complete_degree=data.get('complete_degree', True),
            created_by=data.get('created_by'),
            modified_by=data.get('modified_by')
        )
        db.session.add(education)
        db.session.commit()
        return education, 201

@ns.route('/<string:education_id>')
class EducationDetail(Resource):
    @ns.marshal_with(education_model)
    def get(self, education_id):
        """Get a specific education record"""
        education = Education.query.get_or_404(education_id)
        return education
    
    @ns.expect(education_model)
    @ns.marshal_with(education_model)
    def put(self, education_id):
        """Update a specific education record"""
        education = Education.query.get_or_404(education_id)
        data = request.json
        
        education.school = data.get('school', education.school)
        education.degree = data.get('degree', education.degree)
        education.major = data.get('major', education.major)
        if data.get('start'):
            education.start = datetime.fromisoformat(data['start'].replace('Z', '+00:00'))
        if data.get('end'):
            education.end = datetime.fromisoformat(data['end'].replace('Z', '+00:00'))
        education.grade = data.get('grade', education.grade)
        education.complete_degree = data.get('complete_degree', education.complete_degree)
        education.modified_by = data.get('modified_by')
        
        db.session.commit()
        return education
    
    def delete(self, education_id):
        """Delete a specific education record"""
        education = Education.query.get_or_404(education_id)
        db.session.delete(education)
        db.session.commit()
        return {'message': 'Education record deleted successfully'}, 204

@ns.route('/resume/<string:resume_id>')
class EducationByResume(Resource):
    @ns.marshal_list_with(education_model)
    def get(self, resume_id):
        """Get all education records for a specific resume"""
        education_records = Education.query.filter_by(resume_id=resume_id).all()
        return education_records
