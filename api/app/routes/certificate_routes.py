from flask import request
from flask_restx import Namespace, Resource, fields
from app import db
from app.models import Certificate
from datetime import datetime

ns = Namespace('certificates', description='Certificate operations')

# Model definitions for Swagger
certificate_model = ns.model('Certificate', {
    'id': fields.String(required=False, description='Certificate ID'),
    'resume_id': fields.String(required=True, description='Resume ID'),
    'certificate': fields.String(required=True, description='Certificate name'),
    'certificate_authority': fields.String(required=False, description='Certificate authority'),
    'not_expired': fields.Boolean(required=False, description='Not expired flag'),
    'issue_date': fields.DateTime(required=False, description='Issue date'),
    'expiration_date': fields.DateTime(required=False, description='Expiration date'),
    'score': fields.String(required=False, description='Score'),
    'license_no': fields.String(required=False, description='License number'),
    'certificate_url': fields.String(required=False, description='Certificate URL'),
    'foreign_language': fields.String(required=False, description='Foreign language'),
    'subject': fields.String(required=False, description='Subject'),
    'is_ctc_sponsor': fields.Boolean(required=False, description='CTC sponsor flag'),
    'grade': fields.String(required=False, description='Grade'),
    'provider': fields.String(required=False, description='Provider'),
    'field': fields.String(required=False, description='Field'),
    'sub_field': fields.String(required=False, description='Sub field'),
    'level': fields.String(required=False, description='Level'),
    'status': fields.Integer(required=False, description='Status'),
    'attendance': fields.Boolean(required=False, description='Attendance'),
    'file_name': fields.String(required=False, description='File name'),
    'is_synced': fields.Boolean(required=False, description='Synced flag'),
    'is_education': fields.Boolean(required=False, description='Education flag'),
    'tech_type': fields.String(required=False, description='Tech type'),
    'reject_reason': fields.String(required=False, description='Reject reason'),
    'is_not_has_license_number': fields.Boolean(required=False, description='No license number flag'),
    'created_on': fields.DateTime(required=False, description='Created date'),
    'created_by': fields.String(required=False, description='Created by'),
    'modified_on': fields.DateTime(required=False, description='Modified date'),
    'modified_by': fields.String(required=False, description='Modified by')
})

@ns.route('/')
class CertificateList(Resource):
    @ns.marshal_list_with(certificate_model)
    def get(self):
        """Get all certificates"""
        certificates = Certificate.query.all()
        return certificates
    
    @ns.expect(certificate_model)
    @ns.marshal_with(certificate_model, code=201)
    def post(self):
        """Create a new certificate"""
        data = request.json
        certificate = Certificate(
            resume_id=data['resume_id'],
            certificate=data['certificate'],
            certificate_authority=data.get('certificate_authority'),
            not_expired=data.get('not_expired', True),
            issue_date=datetime.fromisoformat(data['issue_date'].replace('Z', '+00:00')) if data.get('issue_date') else None,
            expiration_date=datetime.fromisoformat(data['expiration_date'].replace('Z', '+00:00')) if data.get('expiration_date') else None,
            score=data.get('score'),
            license_no=data.get('license_no'),
            certificate_url=data.get('certificate_url'),
            foreign_language=data.get('foreign_language'),
            subject=data.get('subject'),
            is_ctc_sponsor=data.get('is_ctc_sponsor', False),
            grade=data.get('grade'),
            provider=data.get('provider'),
            field=data.get('field'),
            sub_field=data.get('sub_field'),
            level=data.get('level'),
            status=data.get('status', 0),
            attendance=data.get('attendance', True),
            file_name=data.get('file_name'),
            is_synced=data.get('is_synced', False),
            is_education=data.get('is_education', False),
            tech_type=data.get('tech_type'),
            reject_reason=data.get('reject_reason'),
            is_not_has_license_number=data.get('is_not_has_license_number', False),
            created_by=data.get('created_by'),
            modified_by=data.get('modified_by')
        )
        db.session.add(certificate)
        db.session.commit()
        return certificate, 201

@ns.route('/<string:certificate_id>')
class CertificateDetail(Resource):
    @ns.marshal_with(certificate_model)
    def get(self, certificate_id):
        """Get a specific certificate"""
        certificate = Certificate.query.get_or_404(certificate_id)
        return certificate
    
    @ns.expect(certificate_model)
    @ns.marshal_with(certificate_model)
    def put(self, certificate_id):
        """Update a specific certificate"""
        certificate = Certificate.query.get_or_404(certificate_id)
        data = request.json
        
        certificate.certificate = data.get('certificate', certificate.certificate)
        certificate.certificate_authority = data.get('certificate_authority', certificate.certificate_authority)
        certificate.not_expired = data.get('not_expired', certificate.not_expired)
        if data.get('issue_date'):
            certificate.issue_date = datetime.fromisoformat(data['issue_date'].replace('Z', '+00:00'))
        if data.get('expiration_date'):
            certificate.expiration_date = datetime.fromisoformat(data['expiration_date'].replace('Z', '+00:00'))
        certificate.score = data.get('score', certificate.score)
        certificate.license_no = data.get('license_no', certificate.license_no)
        certificate.certificate_url = data.get('certificate_url', certificate.certificate_url)
        certificate.foreign_language = data.get('foreign_language', certificate.foreign_language)
        certificate.subject = data.get('subject', certificate.subject)
        certificate.is_ctc_sponsor = data.get('is_ctc_sponsor', certificate.is_ctc_sponsor)
        certificate.grade = data.get('grade', certificate.grade)
        certificate.provider = data.get('provider', certificate.provider)
        certificate.field = data.get('field', certificate.field)
        certificate.sub_field = data.get('sub_field', certificate.sub_field)
        certificate.level = data.get('level', certificate.level)
        certificate.status = data.get('status', certificate.status)
        certificate.attendance = data.get('attendance', certificate.attendance)
        certificate.file_name = data.get('file_name', certificate.file_name)
        certificate.is_synced = data.get('is_synced', certificate.is_synced)
        certificate.is_education = data.get('is_education', certificate.is_education)
        certificate.tech_type = data.get('tech_type', certificate.tech_type)
        certificate.reject_reason = data.get('reject_reason', certificate.reject_reason)
        certificate.is_not_has_license_number = data.get('is_not_has_license_number', certificate.is_not_has_license_number)
        certificate.modified_by = data.get('modified_by')
        
        db.session.commit()
        return certificate
    
    def delete(self, certificate_id):
        """Delete a specific certificate"""
        certificate = Certificate.query.get_or_404(certificate_id)
        db.session.delete(certificate)
        db.session.commit()
        return {'message': 'Certificate deleted successfully'}, 204

@ns.route('/resume/<string:resume_id>')
class CertificateByResume(Resource):
    @ns.marshal_list_with(certificate_model)
    def get(self, resume_id):
        """Get all certificates for a specific resume"""
        certificates = Certificate.query.filter_by(resume_id=resume_id).all()
        return certificates
