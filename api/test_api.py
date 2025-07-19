"""
Simple test examples for the Interview Co-Pilot API
Run these after starting the server with: python run.py
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_resume_crud():
    print("Testing Resume CRUD operations...")
    
    # Create a resume
    resume_data = {
        "first_name": "John",
        "last_name": "Doe",
        "created_by": "admin"
    }
    
    response = requests.post(f"{BASE_URL}/resumes/", json=resume_data)
    print(f"Create Resume: {response.status_code}")
    
    if response.status_code == 201:
        resume = response.json()
        resume_id = resume['id']
        print(f"Created Resume ID: {resume_id}")
        
        # Get the resume
        response = requests.get(f"{BASE_URL}/resumes/{resume_id}")
        print(f"Get Resume: {response.status_code}")
        
        # Update the resume
        update_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "modified_by": "admin"
        }
        response = requests.put(f"{BASE_URL}/resumes/{resume_id}", json=update_data)
        print(f"Update Resume: {response.status_code}")
        
        # Test education for this resume
        test_education_crud(resume_id)
        
        return resume_id
    
    return None

def test_education_crud(resume_id):
    print("Testing Education CRUD operations...")
    
    education_data = {
        "resume_id": resume_id,
        "school": "University of Technology",
        "degree": "Bachelor of Science",
        "major": "Computer Science",
        "start": "2018-09-01T00:00:00",
        "end": "2022-06-30T00:00:00",
        "grade": "3.8",
        "complete_degree": True,
        "created_by": "admin"
    }
    
    response = requests.post(f"{BASE_URL}/education/", json=education_data)
    print(f"Create Education: {response.status_code}")
    
    if response.status_code == 201:
        education = response.json()
        education_id = education['id']
        print(f"Created Education ID: {education_id}")
        
        # Get education by resume
        response = requests.get(f"{BASE_URL}/education/resume/{resume_id}")
        print(f"Get Education by Resume: {response.status_code}")
        if response.status_code == 200:
            print(f"Education records found: {len(response.json())}")

def test_certificate_crud(resume_id):
    print("Testing Certificate CRUD operations...")
    
    certificate_data = {
        "resume_id": resume_id,
        "certificate": "AWS Certified Solutions Architect",
        "certificate_authority": "Amazon Web Services",
        "not_expired": True,
        "issue_date": "2023-01-15T00:00:00",
        "provider": "AWS",
        "field": "Cloud Computing",
        "level": "Associate",
        "created_by": "admin"
    }
    
    response = requests.post(f"{BASE_URL}/certificates/", json=certificate_data)
    print(f"Create Certificate: {response.status_code}")
    
    if response.status_code == 201:
        certificate = response.json()
        print(f"Created Certificate ID: {certificate['id']}")

def test_language_crud(resume_id):
    print("Testing Language CRUD operations...")
    
    # First create a language
    language_data = {
        "name": "English",
        "created_by": "admin"
    }
    
    response = requests.post(f"{BASE_URL}/languages/", json=language_data)
    print(f"Create Language: {response.status_code}")
    
    if response.status_code == 201:
        language = response.json()
        language_id = language['id']
        
        # Create language skill
        skill_data = {
            "resume_id": resume_id,
            "language_id": language_id,
            "proficiency": 5,
            "created_by": "admin"
        }
        
        response = requests.post(f"{BASE_URL}/languages/skills", json=skill_data)
        print(f"Create Language Skill: {response.status_code}")

def test_project_crud(resume_id):
    print("Testing Project CRUD operations...")
    
    project_data = {
        "resume_id": resume_id,
        "name": "E-commerce Platform",
        "project_category": "Development",
        "company": "Tech Corp",
        "type": "External",
        "team_size": 5,
        "technology": ["Python", "Flask", "PostgreSQL", "React"],
        "project_description": "Developed a full-stack e-commerce platform",
        "status": "Completed",
        "domain": "E-commerce",
        "start_date": "2023-01-01T00:00:00",
        "end_date": "2023-06-30T00:00:00",
        "responsibility": "Backend development and API design",
        "skill": "Python Developer",
        "seniority": "Senior",
        "created_by": "admin"
    }
    
    response = requests.post(f"{BASE_URL}/projects/", json=project_data)
    print(f"Create Project: {response.status_code}")
    
    if response.status_code == 201:
        project = response.json()
        print(f"Created Project ID: {project['id']}")

def test_professional_skill_crud(resume_id):
    print("Testing Professional Skill CRUD operations...")
    
    skill_data = {
        "resume_id": resume_id,
        "job_title_name": "Python Developer",
        "experience_year": 3,
        "experience_month": 6,
        "is_main_skill": True,
        "project_info": [{"project": "E-commerce Platform", "role": "Senior Developer"}],
        "created_by": "admin"
    }
    
    response = requests.post(f"{BASE_URL}/professional-skills/", json=skill_data)
    print(f"Create Professional Skill: {response.status_code}")
    
    if response.status_code == 201:
        skill = response.json()
        print(f"Created Professional Skill ID: {skill['id']}")

def main():
    print("Starting API tests...")
    print("Make sure the server is running on http://localhost:5000")
    print("=" * 50)
    
    try:
        # Test if server is running
        response = requests.get(f"{BASE_URL}/")
        print(f"Server status: {response.status_code}")
        
        resume_id = test_resume_crud()
        
        if resume_id:
            test_certificate_crud(resume_id)
            test_language_crud(resume_id)
            test_project_crud(resume_id)
            test_professional_skill_crud(resume_id)
            
            print("=" * 50)
            print("All tests completed!")
            print(f"Check Swagger documentation at: {BASE_URL}/swagger/")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Make sure the server is running with: python run.py")

if __name__ == "__main__":
    main()
