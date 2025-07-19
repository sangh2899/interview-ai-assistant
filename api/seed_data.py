"""
Seed data script for Interview Co-Pilot API
Adds sample data for all models to test the API functionality
"""

from app import create_app, db
from app.models import (
    Resume, Education, Certificate, Language, LanguageSkill, 
    Domain, Project, ProfessionalSkill
)
from datetime import datetime, timedelta
import uuid

app = create_app()

def create_sample_data():
    """Create comprehensive sample data for all models"""
    
    print("Creating sample data...")
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.session.query(ProfessionalSkill).delete()
        db.session.query(Project).delete()
        db.session.query(Domain).delete()
        db.session.query(LanguageSkill).delete()
        db.session.query(Language).delete()
        db.session.query(Certificate).delete()
        db.session.query(Education).delete()
        db.session.query(Resume).delete()
        db.session.commit()
        
        # Create Languages first (referenced by LanguageSkill)
        print("Creating languages...")
        languages = [
            Language(name="English"),
            Language(name="Spanish"),
            Language(name="French"),
            Language(name="German"),
            Language(name="Mandarin"),
            Language(name="Japanese"),
            Language(name="Portuguese"),
            Language(name="Russian")
        ]
        
        for lang in languages:
            db.session.add(lang)
        db.session.commit()
        
        # Create Resumes
        print("Creating resumes...")
        resumes_data = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-0101",
                "summary": "Senior Software Engineer with 5+ years of experience in full-stack development using Python, React, and cloud technologies. Led teams of 5+ developers and delivered scalable solutions for enterprise clients.",
                "created_by": "admin"
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "phone": "+1-555-0102",
                "summary": "Full-Stack Developer specializing in JavaScript frameworks and Node.js backend development. 4+ years of experience building responsive web applications and RESTful APIs.",
                "created_by": "admin"
            },
            {
                "first_name": "Michael",
                "last_name": "Johnson",
                "email": "michael.johnson@example.com",
                "phone": "+1-555-0103",
                "summary": "DevOps Engineer with expertise in AWS, Docker, and Kubernetes. 6+ years of experience in automating deployment pipelines and managing cloud infrastructure.",
                "created_by": "admin"
            },
            {
                "first_name": "Sarah",
                "last_name": "Williams",
                "email": "sarah.williams@example.com",
                "phone": "+1-555-0104",
                "summary": "Data Scientist with strong background in machine learning and statistical analysis. 3+ years of experience using Python, R, and SQL to derive insights from complex datasets.",
                "created_by": "admin"
            },
            {
                "first_name": "David",
                "last_name": "Brown",
                "email": "david.brown@example.com",
                "phone": "+1-555-0105",
                "summary": "Mobile App Developer specializing in iOS and Android development. 4+ years of experience building native and cross-platform mobile applications using Swift, Kotlin, and React Native.",
                "created_by": "admin"
            }
        ]
        
        resumes = []
        for resume_data in resumes_data:
            resume = Resume(**resume_data)
            db.session.add(resume)
            resumes.append(resume)
        db.session.commit()
        
        # Create Education records
        print("Creating education records...")
        education_data = [
            {
                "resume": resumes[0],
                "school": "Massachusetts Institute of Technology",
                "degree": "Master of Science",
                "major": "Computer Science",
                "start": datetime(2018, 9, 1),
                "end": datetime(2020, 6, 30),
                "grade": "3.9",
                "complete_degree": True,
                "created_by": "admin"
            },
            {
                "resume": resumes[0],
                "school": "University of California, Berkeley",
                "degree": "Bachelor of Science",
                "major": "Computer Engineering",
                "start": datetime(2014, 9, 1),
                "end": datetime(2018, 5, 30),
                "grade": "3.7",
                "complete_degree": True,
                "created_by": "admin"
            },
            {
                "resume": resumes[1],
                "school": "Stanford University",
                "degree": "Master of Business Administration",
                "major": "Technology Management",
                "start": datetime(2019, 9, 1),
                "end": datetime(2021, 6, 30),
                "grade": "3.8",
                "complete_degree": True,
                "created_by": "admin"
            },
            {
                "resume": resumes[1],
                "school": "University of Washington",
                "degree": "Bachelor of Science",
                "major": "Information Systems",
                "start": datetime(2015, 9, 1),
                "end": datetime(2019, 5, 30),
                "grade": "3.6",
                "complete_degree": True,
                "created_by": "admin"
            },
            {
                "resume": resumes[2],
                "school": "Carnegie Mellon University",
                "degree": "Bachelor of Science",
                "major": "Software Engineering",
                "start": datetime(2016, 9, 1),
                "end": datetime(2020, 5, 30),
                "grade": "3.8",
                "complete_degree": True,
                "created_by": "admin"
            }
        ]
        
        for edu_data in education_data:
            education = Education(
                resume_id=edu_data["resume"].id,
                school=edu_data["school"],
                degree=edu_data["degree"],
                major=edu_data["major"],
                start=edu_data["start"],
                end=edu_data["end"],
                grade=edu_data["grade"],
                complete_degree=edu_data["complete_degree"],
                created_by=edu_data["created_by"]
            )
            db.session.add(education)
        db.session.commit()
        
        # Create Certificates
        print("Creating certificates...")
        certificates_data = [
            {
                "resume": resumes[0],
                "certificate": "AWS Certified Solutions Architect",
                "certificate_authority": "Amazon Web Services",
                "not_expired": True,
                "issue_date": datetime(2023, 1, 15),
                "provider": "AWS",
                "field": "Cloud Computing",
                "level": "Professional",
                "created_by": "admin"
            },
            {
                "resume": resumes[0],
                "certificate": "Certified Kubernetes Administrator",
                "certificate_authority": "Cloud Native Computing Foundation",
                "not_expired": True,
                "issue_date": datetime(2022, 8, 20),
                "provider": "CNCF",
                "field": "Container Orchestration",
                "level": "Professional",
                "created_by": "admin"
            },
            {
                "resume": resumes[1],
                "certificate": "Google Cloud Professional Data Engineer",
                "certificate_authority": "Google",
                "not_expired": True,
                "issue_date": datetime(2023, 3, 10),
                "provider": "Google Cloud",
                "field": "Data Engineering",
                "level": "Professional",
                "created_by": "admin"
            },
            {
                "resume": resumes[2],
                "certificate": "Microsoft Azure Developer Associate",
                "certificate_authority": "Microsoft",
                "not_expired": True,
                "issue_date": datetime(2022, 11, 5),
                "provider": "Microsoft",
                "field": "Cloud Development",
                "level": "Associate",
                "created_by": "admin"
            },
            {
                "resume": resumes[3],
                "certificate": "Certified Scrum Master",
                "certificate_authority": "Scrum Alliance",
                "not_expired": True,
                "issue_date": datetime(2023, 2, 28),
                "provider": "Scrum Alliance",
                "field": "Project Management",
                "level": "Professional",
                "created_by": "admin"
            }
        ]
        
        for cert_data in certificates_data:
            certificate = Certificate(
                resume_id=cert_data["resume"].id,
                certificate=cert_data["certificate"],
                certificate_authority=cert_data["certificate_authority"],
                not_expired=cert_data["not_expired"],
                issue_date=cert_data["issue_date"],
                provider=cert_data["provider"],
                field=cert_data["field"],
                level=cert_data["level"],
                created_by=cert_data["created_by"]
            )
            db.session.add(certificate)
        db.session.commit()
        
        # Create Language Skills
        print("Creating language skills...")
        language_skills_data = [
            {"resume": resumes[0], "language": languages[0], "proficiency": 5},  # English - Native
            {"resume": resumes[0], "language": languages[1], "proficiency": 4},  # Spanish - Fluent
            {"resume": resumes[0], "language": languages[2], "proficiency": 3},  # French - Intermediate
            {"resume": resumes[1], "language": languages[0], "proficiency": 5},  # English - Native
            {"resume": resumes[1], "language": languages[4], "proficiency": 3},  # Mandarin - Intermediate
            {"resume": resumes[2], "language": languages[0], "proficiency": 5},  # English - Native
            {"resume": resumes[2], "language": languages[3], "proficiency": 4},  # German - Fluent
            {"resume": resumes[3], "language": languages[0], "proficiency": 5},  # English - Native
            {"resume": resumes[3], "language": languages[5], "proficiency": 3},  # Japanese - Intermediate
            {"resume": resumes[4], "language": languages[0], "proficiency": 5},  # English - Native
            {"resume": resumes[4], "language": languages[6], "proficiency": 4},  # Portuguese - Fluent
        ]
        
        for lang_skill_data in language_skills_data:
            lang_skill = LanguageSkill(
                resume_id=lang_skill_data["resume"].id,
                language_id=lang_skill_data["language"].id,
                proficiency=lang_skill_data["proficiency"],
                created_by="admin"
            )
            db.session.add(lang_skill)
        db.session.commit()
        
        # Create Domain Experience
        print("Creating domain experience...")
        domains_data = [
            {"resume": resumes[0], "name": "Financial Technology", "year": 3, "month": 6},
            {"resume": resumes[0], "name": "E-commerce", "year": 2, "month": 0},
            {"resume": resumes[1], "name": "Healthcare Technology", "year": 4, "month": 3},
            {"resume": resumes[1], "name": "Data Analytics", "year": 3, "month": 0},
            {"resume": resumes[2], "name": "Gaming", "year": 2, "month": 8},
            {"resume": resumes[2], "name": "Mobile Applications", "year": 3, "month": 0},
            {"resume": resumes[3], "name": "Enterprise Software", "year": 5, "month": 0},
            {"resume": resumes[3], "name": "DevOps", "year": 2, "month": 6},
            {"resume": resumes[4], "name": "Artificial Intelligence", "year": 1, "month": 10},
            {"resume": resumes[4], "name": "Machine Learning", "year": 2, "month": 4},
        ]
        
        for domain_data in domains_data:
            domain = Domain(
                resume_id=domain_data["resume"].id,
                name=domain_data["name"],
                year=domain_data["year"],
                month=domain_data["month"],
                created_by="admin"
            )
            db.session.add(domain)
        db.session.commit()
        
        # Create Projects
        print("Creating projects...")
        projects_data = [
            {
                "resume": resumes[0],
                "name": "Banking Payment System",
                "project_category": "Development",
                "company": "FinTech Solutions Inc",
                "type": "External",
                "team_size": 8,
                "technology": ["Java", "Spring Boot", "PostgreSQL", "React", "AWS"],
                "project_description": "Developed a secure payment processing system for online banking with real-time transaction processing capabilities.",
                "status": "Completed",
                "domain": "Financial Technology",
                "start_date": datetime(2022, 1, 15),
                "end_date": datetime(2023, 6, 30),
                "responsibility": "Lead Backend Developer - Designed microservices architecture, implemented payment APIs, and ensured PCI DSS compliance.",
                "skill": "Java Developer",
                "seniority": "Senior",
                "created_by": "admin"
            },
            {
                "resume": resumes[0],
                "name": "E-commerce Platform Modernization",
                "project_category": "Maintenance",
                "company": "ShopTech Corp",
                "type": "External",
                "team_size": 12,
                "technology": ["Python", "Django", "Redis", "Elasticsearch", "Docker"],
                "project_description": "Modernized legacy e-commerce platform to improve performance and scalability.",
                "status": "Completed",
                "domain": "E-commerce",
                "start_date": datetime(2021, 3, 1),
                "end_date": datetime(2022, 1, 10),
                "responsibility": "Full Stack Developer - Migrated legacy systems, optimized database queries, and implemented caching strategies.",
                "skill": "Python Developer",
                "seniority": "Senior",
                "created_by": "admin"
            },
            {
                "resume": resumes[1],
                "name": "Healthcare Data Analytics Platform",
                "project_category": "Development",
                "company": "MedTech Innovations",
                "type": "External",
                "team_size": 15,
                "technology": ["Python", "TensorFlow", "Apache Spark", "Kafka", "MongoDB"],
                "project_description": "Built a comprehensive data analytics platform for healthcare providers to analyze patient data and treatment outcomes.",
                "status": "On-going",
                "domain": "Healthcare Technology",
                "start_date": datetime(2023, 2, 1),
                "end_date": None,
                "responsibility": "Data Engineering Lead - Designed data pipelines, implemented ML models for predictive analytics, and managed data governance.",
                "skill": "Data Engineer",
                "seniority": "Senior",
                "created_by": "admin"
            },
            {
                "resume": resumes[2],
                "name": "Mobile Gaming Platform",
                "project_category": "Development",
                "company": "GameStudio Pro",
                "type": "External",
                "team_size": 20,
                "technology": ["Unity", "C#", "Firebase", "Node.js", "GraphQL"],
                "project_description": "Developed a multiplayer mobile gaming platform with real-time gameplay and social features.",
                "status": "Completed",
                "domain": "Gaming",
                "start_date": datetime(2022, 6, 1),
                "end_date": datetime(2023, 12, 15),
                "responsibility": "Game Developer - Implemented gameplay mechanics, optimized performance, and integrated social features.",
                "skill": "Unity Developer",
                "seniority": "Mid-level",
                "created_by": "admin"
            },
            {
                "resume": resumes[3],
                "name": "Enterprise Resource Planning System",
                "project_category": "Development",
                "company": "Enterprise Solutions Ltd",
                "type": "Internal",
                "team_size": 25,
                "technology": ["Java", "Spring Framework", "Oracle", "Angular", "Jenkins"],
                "project_description": "Built a comprehensive ERP system for large enterprises to manage resources, finances, and operations.",
                "status": "Completed",
                "domain": "Enterprise Software",
                "start_date": datetime(2021, 8, 1),
                "end_date": datetime(2023, 3, 30),
                "responsibility": "Technical Lead - Architected the system, led development team, and ensured quality delivery.",
                "skill": "Java Architect",
                "seniority": "Senior",
                "created_by": "admin"
            }
        ]
        
        for project_data in projects_data:
            project = Project(
                resume_id=project_data["resume"].id,
                name=project_data["name"],
                project_category=project_data["project_category"],
                company=project_data["company"],
                type=project_data["type"],
                team_size=project_data["team_size"],
                technology=project_data["technology"],
                project_description=project_data["project_description"],
                status=project_data["status"],
                domain=project_data["domain"],
                start_date=project_data["start_date"],
                end_date=project_data["end_date"],
                responsibility=project_data["responsibility"],
                skill=project_data["skill"],
                seniority=project_data["seniority"],
                created_by=project_data["created_by"]
            )
            db.session.add(project)
        db.session.commit()
        
        # Create Professional Skills
        print("Creating professional skills...")
        skills_data = [
            {
                "resume": resumes[0],
                "job_title_name": "Java Developer",
                "experience_year": 5,
                "experience_month": 6,
                "is_main_skill": True,
                "project_info": [
                    {"project": "Banking Payment System", "role": "Lead Developer"},
                    {"project": "E-commerce Platform", "role": "Backend Developer"}
                ]
            },
            {
                "resume": resumes[0],
                "job_title_name": "Python Developer",
                "experience_year": 3,
                "experience_month": 0,
                "is_main_skill": False,
                "project_info": [
                    {"project": "E-commerce Platform Modernization", "role": "Full Stack Developer"}
                ]
            },
            {
                "resume": resumes[1],
                "job_title_name": "Data Engineer",
                "experience_year": 4,
                "experience_month": 3,
                "is_main_skill": True,
                "project_info": [
                    {"project": "Healthcare Data Analytics Platform", "role": "Lead Data Engineer"}
                ]
            },
            {
                "resume": resumes[1],
                "job_title_name": "Machine Learning Engineer",
                "experience_year": 2,
                "experience_month": 8,
                "is_main_skill": False,
                "project_info": [
                    {"project": "Predictive Analytics Module", "role": "ML Engineer"}
                ]
            },
            {
                "resume": resumes[2],
                "job_title_name": "Unity Developer",
                "experience_year": 3,
                "experience_month": 4,
                "is_main_skill": True,
                "project_info": [
                    {"project": "Mobile Gaming Platform", "role": "Game Developer"}
                ]
            },
            {
                "resume": resumes[3],
                "job_title_name": "Java Architect",
                "experience_year": 6,
                "experience_month": 0,
                "is_main_skill": True,
                "project_info": [
                    {"project": "Enterprise Resource Planning System", "role": "Technical Lead"}
                ]
            },
            {
                "resume": resumes[4],
                "job_title_name": "AI Research Engineer",
                "experience_year": 2,
                "experience_month": 6,
                "is_main_skill": True,
                "project_info": [
                    {"project": "Natural Language Processing System", "role": "Research Engineer"}
                ]
            }
        ]
        
        for skill_data in skills_data:
            skill = ProfessionalSkill(
                resume_id=skill_data["resume"].id,
                job_title_name=skill_data["job_title_name"],
                experience_year=skill_data["experience_year"],
                experience_month=skill_data["experience_month"],
                is_main_skill=skill_data["is_main_skill"],
                project_info=skill_data["project_info"],
                created_by="admin"
            )
            db.session.add(skill)
        db.session.commit()
        
        print("Sample data creation completed successfully!")
        print(f"Created:")
        print(f"  - {len(resumes)} resumes")
        print(f"  - {len(languages)} languages")
        print(f"  - {len(education_data)} education records")
        print(f"  - {len(certificates_data)} certificates")
        print(f"  - {len(language_skills_data)} language skills")
        print(f"  - {len(domains_data)} domain experiences")
        print(f"  - {len(projects_data)} projects")
        print(f"  - {len(skills_data)} professional skills")

if __name__ == "__main__":
    create_sample_data()
