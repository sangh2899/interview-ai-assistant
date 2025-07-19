from flask import request
from flask_restx import Namespace, Resource, fields
from app import db
from app.models import Resume, Education, Certificate, LanguageSkill, Language, Domain, Project, ProfessionalSkill

ns = Namespace('resumes', description='Resume operations')

# Model definitions for Swagger
resume_model = ns.model('Resume', {
    'id': fields.String(required=False, description='Resume ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=False, description='Email address'),
    'phone': fields.String(required=False, description='Phone number'),
    'summary': fields.String(required=False, description='Professional summary'),
    'created_on': fields.DateTime(required=False, description='Created date'),
    'created_by': fields.String(required=False, description='Created by'),
    'modified_on': fields.DateTime(required=False, description='Modified date'),
    'modified_by': fields.String(required=False, description='Modified by')
})

@ns.route('/')
class ResumeList(Resource):
    @ns.marshal_list_with(resume_model)
    def get(self):
        """Get all resumes"""
        resumes = Resume.query.all()
        return resumes
    
    @ns.expect(resume_model)
    @ns.marshal_with(resume_model, code=201)
    def post(self):
        """Create a new resume"""
        data = request.json
        resume = Resume(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data.get('email'),
            phone=data.get('phone'),
            summary=data.get('summary'),
            created_by=data.get('created_by'),
            modified_by=data.get('modified_by')
        )
        db.session.add(resume)
        db.session.commit()
        return resume, 201

@ns.route('/<string:resume_id>')
class ResumeDetail(Resource):
    @ns.marshal_with(resume_model)
    def get(self, resume_id):
        """Get a specific resume"""
        resume = Resume.query.get_or_404(resume_id)
        return resume
    
    @ns.expect(resume_model)
    @ns.marshal_with(resume_model)
    def put(self, resume_id):
        """Update a specific resume"""
        resume = Resume.query.get_or_404(resume_id)
        data = request.json
        
        resume.first_name = data.get('first_name', resume.first_name)
        resume.last_name = data.get('last_name', resume.last_name)
        resume.email = data.get('email', resume.email)
        resume.phone = data.get('phone', resume.phone)
        resume.summary = data.get('summary', resume.summary)
        resume.modified_by = data.get('modified_by')
        
        db.session.commit()
        return resume
    
    def delete(self, resume_id):
        """Delete a specific resume"""
        resume = Resume.query.get_or_404(resume_id)
        db.session.delete(resume)
        db.session.commit()
        return {'message': 'Resume deleted successfully'}, 204

@ns.route('/<string:resume_id>/full')
class ResumeFullData(Resource):
    def get(self, resume_id):
        """Get complete resume data with all related information in nested structure"""
        resume = Resume.query.get_or_404(resume_id)
        
        # Helper function to format datetime fields
        def format_datetime(dt):
            return dt.isoformat() if dt else None
        
        # Build the nested response structure
        response_data = {
            "id": resume.id,
            "first_name": resume.first_name,
            "last_name": resume.last_name,
            "email": resume.email,
            "phone": resume.phone,
            "summary": resume.summary,
            "created_on": format_datetime(resume.created_on),
            "created_by": resume.created_by,
            "modified_on": format_datetime(resume.modified_on),
            "modified_by": resume.modified_by,
            "educations": [],
            "certificates": [],
            "languages": [],
            "domains": [],
            "projects": [],
            "professional_skills": []
        }
        
        # Add education data
        for education in resume.educations:
            education_data = {
                "id": education.id,
                "school": education.school,
                "degree": education.degree,
                "major": education.major,
                "start": format_datetime(education.start),
                "end": format_datetime(education.end),
                "grade": education.grade,
                "complete_degree": education.complete_degree,
                "created_on": format_datetime(education.created_on),
                "created_by": education.created_by,
                "modified_on": format_datetime(education.modified_on),
                "modified_by": education.modified_by
            }
            response_data["educations"].append(education_data)
        
        # Add certificate data
        for certificate in resume.certificates:
            certificate_data = {
                "id": certificate.id,
                "certificate": certificate.certificate,
                "certificate_authority": certificate.certificate_authority,
                "not_expired": certificate.not_expired,
                "issue_date": format_datetime(certificate.issue_date),
                "expiration_date": format_datetime(certificate.expiration_date),
                "score": certificate.score,
                "license_no": certificate.license_no,
                "certificate_url": certificate.certificate_url,
                "foreign_language": certificate.foreign_language,
                "subject": certificate.subject,
                "is_ctc_sponsor": certificate.is_ctc_sponsor,
                "grade": certificate.grade,
                "certificate_catalog_id": certificate.certificate_catalog_id,
                "provider_id": certificate.provider_id,
                "provider": certificate.provider,
                "field_id": certificate.field_id,
                "field": certificate.field,
                "sub_field_id": certificate.sub_field_id,
                "sub_field": certificate.sub_field,
                "level_id": certificate.level_id,
                "level": certificate.level,
                "status": certificate.status,
                "attendance": certificate.attendance,
                "file_name": certificate.file_name,
                "is_synced": certificate.is_synced,
                "is_education": certificate.is_education,
                "tech_type": certificate.tech_type,
                "reject_reason": certificate.reject_reason,
                "is_not_has_license_number": certificate.is_not_has_license_number,
                "created_on": format_datetime(certificate.created_on),
                "created_by": certificate.created_by,
                "modified_on": format_datetime(certificate.modified_on),
                "modified_by": certificate.modified_by
            }
            response_data["certificates"].append(certificate_data)
        
        # Add language data with nested language information
        for language_skill in resume.languages:
            language_data = {
                "id": language_skill.id,
                "language_id": language_skill.language_id,
                "proficiency": language_skill.proficiency,
                "created_on": format_datetime(language_skill.created_on),
                "created_by": language_skill.created_by,
                "modified_on": format_datetime(language_skill.modified_on),
                "modified_by": language_skill.modified_by,
                "language": {
                    "id": language_skill.language.id,
                    "name": language_skill.language.name,
                    "created_on": format_datetime(language_skill.language.created_on),
                    "created_by": language_skill.language.created_by,
                    "modified_on": format_datetime(language_skill.language.modified_on),
                    "modified_by": language_skill.language.modified_by
                }
            }
            response_data["languages"].append(language_data)
        
        # Add domain data
        for domain in resume.domains:
            domain_data = {
                "id": domain.id,
                "name": domain.name,
                "year": domain.year,
                "month": domain.month,
                "created_on": format_datetime(domain.created_on),
                "created_by": domain.created_by,
                "modified_on": format_datetime(domain.modified_on),
                "modified_by": domain.modified_by
            }
            response_data["domains"].append(domain_data)
        
        # Add project data
        for project in resume.projects:
            project_data = {
                "id": project.id,
                "resume_project_id": project.resume_project_id,
                "project_id": project.project_id,
                "name": project.name,
                "project_key": project.project_key,
                "project_code": project.project_code,
                "project_rank": project.project_rank,
                "project_lead": project.project_lead,
                "project_category": project.project_category,
                "customer_code": project.customer_code,
                "contract_type": project.contract_type,
                "url": project.url,
                "company": project.company,
                "type": project.type,
                "team_size": project.team_size,
                "search_skill": project.search_skill,
                "technology": project.technology,
                "project_description": project.project_description,
                "groupname": project.groupname,
                "status": project.status,
                "domain": project.domain,
                "start_date": format_datetime(project.start_date),
                "end_date": format_datetime(project.end_date),
                "pain_points": project.pain_points,
                "key_findings": project.key_findings,
                "working_process": project.working_process,
                "responsibility": project.responsibility,
                "technology_by_pm": project.technology_by_pm,
                "description_by_pm": project.description_by_pm,
                "is_update_team": project.is_update_team,
                "apply_incompleted": project.apply_incompleted,
                "skill": project.skill,
                "skill_code": project.skill_code,
                "seniority": project.seniority,
                "created_on": format_datetime(project.created_on),
                "created_by": project.created_by,
                "modified_on": format_datetime(project.modified_on),
                "modified_by": project.modified_by
            }
            response_data["projects"].append(project_data)
        
        # Add professional skills data
        for skill in resume.professional_skills:
            skill_data = {
                "id": skill.id,
                "job_title_name": skill.job_title_name,
                "experience_month": skill.experience_month,
                "experience_year": skill.experience_year,
                "job_fill_by_user": skill.job_fill_by_user,
                "is_main_skill": skill.is_main_skill,
                "project_info": skill.project_info,
                "created_on": format_datetime(skill.created_on),
                "created_by": skill.created_by,
                "modified_on": format_datetime(skill.modified_on),
                "modified_by": skill.modified_by
            }
            response_data["professional_skills"].append(skill_data)
        
        return response_data, 200
