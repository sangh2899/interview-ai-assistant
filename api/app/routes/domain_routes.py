from flask import request
from flask_restx import Namespace, Resource, fields
from app import db
from app.models import Domain

ns = Namespace('domains', description='Domain operations')

# Model definitions for Swagger
domain_model = ns.model('Domain', {
    'id': fields.String(required=False, description='Domain ID'),
    'resume_id': fields.String(required=True, description='Resume ID'),
    'name': fields.String(required=True, description='Domain name'),
    'year': fields.Integer(required=False, description='Years of experience'),
    'month': fields.Integer(required=False, description='Months of experience'),
    'created_on': fields.DateTime(required=False, description='Created date'),
    'created_by': fields.String(required=False, description='Created by'),
    'modified_on': fields.DateTime(required=False, description='Modified date'),
    'modified_by': fields.String(required=False, description='Modified by')
})

@ns.route('/')
class DomainList(Resource):
    @ns.marshal_list_with(domain_model)
    def get(self):
        """Get all domains"""
        domains = Domain.query.all()
        return domains
    
    @ns.expect(domain_model)
    @ns.marshal_with(domain_model, code=201)
    def post(self):
        """Create a new domain"""
        data = request.json
        domain = Domain(
            resume_id=data['resume_id'],
            name=data['name'],
            year=data.get('year', 0),
            month=data.get('month', 0),
            created_by=data.get('created_by'),
            modified_by=data.get('modified_by')
        )
        db.session.add(domain)
        db.session.commit()
        return domain, 201

@ns.route('/<string:domain_id>')
class DomainDetail(Resource):
    @ns.marshal_with(domain_model)
    def get(self, domain_id):
        """Get a specific domain"""
        domain = Domain.query.get_or_404(domain_id)
        return domain
    
    @ns.expect(domain_model)
    @ns.marshal_with(domain_model)
    def put(self, domain_id):
        """Update a specific domain"""
        domain = Domain.query.get_or_404(domain_id)
        data = request.json
        
        domain.name = data.get('name', domain.name)
        domain.year = data.get('year', domain.year)
        domain.month = data.get('month', domain.month)
        domain.modified_by = data.get('modified_by')
        
        db.session.commit()
        return domain
    
    def delete(self, domain_id):
        """Delete a specific domain"""
        domain = Domain.query.get_or_404(domain_id)
        db.session.delete(domain)
        db.session.commit()
        return {'message': 'Domain deleted successfully'}, 204

@ns.route('/resume/<string:resume_id>')
class DomainByResume(Resource):
    @ns.marshal_list_with(domain_model)
    def get(self, resume_id):
        """Get all domains for a specific resume"""
        domains = Domain.query.filter_by(resume_id=resume_id).all()
        return domains
