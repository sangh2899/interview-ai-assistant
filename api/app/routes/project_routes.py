from flask import request
from flask_restx import Namespace, Resource, fields
from app import db
from app.models import Project
from datetime import datetime

ns = Namespace('projects', description='Project operations')

# Model definitions for Swagger
project_model = ns.model('Project', {
    'id': fields.String(required=False, description='Project ID'),
    'resume_id': fields.String(required=True, description='Resume ID'),
    'resume_project_id': fields.String(required=False, description='Resume project ID'),
    'project_id': fields.String(required=False, description='External project ID'),
    'name': fields.String(required=True, description='Project name'),
    'project_key': fields.String(required=False, description='Project key'),
    'project_code': fields.String(required=False, description='Project code'),
    'project_rank': fields.String(required=False, description='Project rank'),
    'project_lead': fields.String(required=False, description='Project lead'),
    'project_category': fields.String(required=False, description='Project category'),
    'customer_code': fields.String(required=False, description='Customer code'),
    'contract_type': fields.String(required=False, description='Contract type'),
    'url': fields.String(required=False, description='Project URL'),
    'company': fields.String(required=False, description='Company'),
    'type': fields.String(required=False, description='Project type'),
    'team_size': fields.Integer(required=False, description='Team size'),
    'search_skill': fields.Integer(required=False, description='Search skill'),
    'technology': fields.List(fields.String, required=False, description='Technologies used'),
    'project_description': fields.String(required=False, description='Project description'),
    'groupname': fields.String(required=False, description='Group name'),
    'status': fields.String(required=False, description='Project status'),
    'domain': fields.String(required=False, description='Domain'),
    'start_date': fields.DateTime(required=False, description='Start date'),
    'end_date': fields.DateTime(required=False, description='End date'),
    'pain_points': fields.String(required=False, description='Pain points'),
    'key_findings': fields.String(required=False, description='Key findings'),
    'working_process': fields.String(required=False, description='Working process'),
    'responsibility': fields.String(required=False, description='Responsibility'),
    'technology_by_pm': fields.String(required=False, description='Technology by PM'),
    'description_by_pm': fields.String(required=False, description='Description by PM'),
    'is_update_team': fields.Boolean(required=False, description='Update team flag'),
    'apply_incompleted': fields.Boolean(required=False, description='Apply incompleted flag'),
    'skill': fields.String(required=False, description='Skill'),
    'skill_code': fields.String(required=False, description='Skill code'),
    'seniority': fields.String(required=False, description='Seniority level'),
    'created_on': fields.DateTime(required=False, description='Created date'),
    'created_by': fields.String(required=False, description='Created by'),
    'modified_on': fields.DateTime(required=False, description='Modified date'),
    'modified_by': fields.String(required=False, description='Modified by')
})

@ns.route('/')
class ProjectList(Resource):
    @ns.marshal_list_with(project_model)
    def get(self):
        """Get all projects"""
        projects = Project.query.all()
        return projects
    
    @ns.expect(project_model)
    @ns.marshal_with(project_model, code=201)
    def post(self):
        """Create a new project"""
        data = request.json
        project = Project(
            resume_id=data['resume_id'],
            resume_project_id=data.get('resume_project_id'),
            project_id=data.get('project_id'),
            name=data['name'],
            project_key=data.get('project_key'),
            project_code=data.get('project_code'),
            project_rank=data.get('project_rank'),
            project_lead=data.get('project_lead'),
            project_category=data.get('project_category'),
            customer_code=data.get('customer_code'),
            contract_type=data.get('contract_type'),
            url=data.get('url'),
            company=data.get('company'),
            type=data.get('type'),
            team_size=data.get('team_size', 0),
            search_skill=data.get('search_skill', 0),
            technology=data.get('technology'),
            project_description=data.get('project_description'),
            groupname=data.get('groupname'),
            status=data.get('status'),
            domain=data.get('domain'),
            start_date=datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')) if data.get('start_date') else None,
            end_date=datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')) if data.get('end_date') else None,
            pain_points=data.get('pain_points'),
            key_findings=data.get('key_findings'),
            working_process=data.get('working_process'),
            responsibility=data.get('responsibility'),
            technology_by_pm=data.get('technology_by_pm'),
            description_by_pm=data.get('description_by_pm'),
            is_update_team=data.get('is_update_team', False),
            apply_incompleted=data.get('apply_incompleted', False),
            skill=data.get('skill'),
            skill_code=data.get('skill_code'),
            seniority=data.get('seniority'),
            created_by=data.get('created_by'),
            modified_by=data.get('modified_by')
        )
        db.session.add(project)
        db.session.commit()
        return project, 201

@ns.route('/<string:project_id>')
class ProjectDetail(Resource):
    @ns.marshal_with(project_model)
    def get(self, project_id):
        """Get a specific project"""
        project = Project.query.get_or_404(project_id)
        return project
    
    @ns.expect(project_model)
    @ns.marshal_with(project_model)
    def put(self, project_id):
        """Update a specific project"""
        project = Project.query.get_or_404(project_id)
        data = request.json
        
        project.name = data.get('name', project.name)
        project.resume_project_id = data.get('resume_project_id', project.resume_project_id)
        project.project_id = data.get('project_id', project.project_id)
        project.project_key = data.get('project_key', project.project_key)
        project.project_code = data.get('project_code', project.project_code)
        project.project_rank = data.get('project_rank', project.project_rank)
        project.project_lead = data.get('project_lead', project.project_lead)
        project.project_category = data.get('project_category', project.project_category)
        project.customer_code = data.get('customer_code', project.customer_code)
        project.contract_type = data.get('contract_type', project.contract_type)
        project.url = data.get('url', project.url)
        project.company = data.get('company', project.company)
        project.type = data.get('type', project.type)
        project.team_size = data.get('team_size', project.team_size)
        project.search_skill = data.get('search_skill', project.search_skill)
        project.technology = data.get('technology', project.technology)
        project.project_description = data.get('project_description', project.project_description)
        project.groupname = data.get('groupname', project.groupname)
        project.status = data.get('status', project.status)
        project.domain = data.get('domain', project.domain)
        if data.get('start_date'):
            project.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        if data.get('end_date'):
            project.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        project.pain_points = data.get('pain_points', project.pain_points)
        project.key_findings = data.get('key_findings', project.key_findings)
        project.working_process = data.get('working_process', project.working_process)
        project.responsibility = data.get('responsibility', project.responsibility)
        project.technology_by_pm = data.get('technology_by_pm', project.technology_by_pm)
        project.description_by_pm = data.get('description_by_pm', project.description_by_pm)
        project.is_update_team = data.get('is_update_team', project.is_update_team)
        project.apply_incompleted = data.get('apply_incompleted', project.apply_incompleted)
        project.skill = data.get('skill', project.skill)
        project.skill_code = data.get('skill_code', project.skill_code)
        project.seniority = data.get('seniority', project.seniority)
        project.modified_by = data.get('modified_by')
        
        db.session.commit()
        return project
    
    def delete(self, project_id):
        """Delete a specific project"""
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return {'message': 'Project deleted successfully'}, 204

@ns.route('/resume/<string:resume_id>')
class ProjectByResume(Resource):
    @ns.marshal_list_with(project_model)
    def get(self, resume_id):
        """Get all projects for a specific resume"""
        projects = Project.query.filter_by(resume_id=resume_id).all()
        return projects
