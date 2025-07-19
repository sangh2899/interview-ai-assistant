"""
Mock data generator for interview agent testing.
Creates sample resumes, job descriptions, and question banks.
Supports both file-based storage and PostgreSQL initialization.
"""

import json
import os
import logging
import uuid
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class Language:
    name: str
    id: str
    createdOn: str
    createdBy: str
    modifiedOn: str
    modifiedBy: str

@dataclass
class LanguageSkill:
    resumeId: str
    proficiency: int
    language: Language
    id: str
    createdOn: str
    createdBy: str
    modifiedOn: str
    modifiedBy: str

@dataclass
class Education:
    resumeId: str
    school: str
    degree: str
    major: str
    start: str
    end: str
    grade: str
    completeDegree: bool
    id: str
    createdOn: str
    createdBy: str
    modifiedOn: str
    modifiedBy: str

@dataclass
class Certificate:
    resumeId: str
    certificate: str
    certificateAuthority: Optional[str]
    notExpired: bool
    issueDate: str
    expirationDate: Optional[str]
    score: Optional[str]
    licenseNo: Optional[str]
    certificateUrl: Optional[str]
    foreignLanguage: Optional[str]
    subject: Optional[str]
    isCTCSponsor: bool
    grade: Optional[str]
    certificateCatalogId: str
    providerId: str
    provider: str
    fieldId: str
    field: str
    subFieldId: str
    subField: str
    levelId: Optional[str]
    level: str
    status: int
    attendance: bool
    fileName: Optional[str]
    isSynced: bool
    isEducation: bool
    techType: Optional[str]
    rejectReason: Optional[str]
    isNotHasLicenseNumber: bool
    id: str
    createdOn: str
    createdBy: str
    modifiedOn: Optional[str]
    modifiedBy: Optional[str]

@dataclass
class Domain:
    name: str
    year: int
    month: int
    resumeId: str
    id: str
    createdOn: str
    createdBy: str
    modifiedOn: str
    modifiedBy: str

@dataclass
class Project:
    resumeId: str
    resumeProjectId: str
    projectId: str
    name: str
    projectKey: str
    projectCode: str
    projectRank: str
    projectLead: str
    projectCategory: str
    customerCode: str
    contractType: str
    url: str
    company: str
    type: str
    teamSize: int
    searchSkill: int
    technology: List[str]
    projectDescription: str
    groupname: str
    status: str
    domain: str
    startDate: str
    endDate: str
    painPoins: Optional[str]
    keyFindings: Optional[str]
    workingProcess: Optional[str]
    responsibility: str
    technologyByPM: Optional[str]
    descriptionByPM: Optional[str]
    isUpdateTeam: bool
    applyIncompleted: bool
    skill: str
    skillCode: Optional[str]
    seniority: Optional[str]
    projectRoles: List
    projectSkills: List
    projectJobs: List

@dataclass
class ProfessionalSkill:
    id: str
    resumeId: str
    jobTitleName: str
    experienceMonth: int
    experienceYear: int
    jobFillByUser: Optional[str]
    isMainSkill: bool
    projectInfo: List

@dataclass
class Resume:
    name: str
    email: str
    phone: str
    summary: str
    education: Education
    certificates: List[Certificate]
    languages: List[LanguageSkill]
    domain: List[Domain]
    projects: List[Project]
    professionalSkills: List[ProfessionalSkill]
    # Keep legacy fields for backward compatibility during transition
    experience: List[Dict[str, str]] = None
    skills: List[str] = None

@dataclass
class JobDescription:
    title: str
    company: str
    department: str
    level: str
    requirements: List[str]
    responsibilities: List[str]
    skills_required: List[str]
    experience_years: str

@dataclass
class QuestionBank:
    category: str
    difficulty: str
    questions: List[Dict[str, str]]

def generate_sample_resumes() -> List[Resume]:
    """Generate sample resumes for different roles with enhanced data."""
    
    resumes = [
        Resume(
            name="John Smith",
            email="john.smith@email.com",
            phone="+1-555-0123",
            summary="Senior Software Engineer with 5+ years of experience in full-stack development using Python, React, and cloud technologies. Led teams of 5+ developers and delivered scalable solutions for enterprise clients.",
            education=Education(
                resumeId=str(uuid.uuid4()),
                school="State University",
                degree="Bachelor of Science in Computer Science",
                major="Computer Science",
                start="2019-09-01",
                end="2023-05-15",
                grade="3.8/4.0",
                completeDegree=True,
                id=str(uuid.uuid4()),
                createdOn=datetime.now().isoformat(),
                createdBy="system",
                modifiedOn=datetime.now().isoformat(),
                modifiedBy="system"
            ),
            certificates=[
                Certificate(
                    resumeId=str(uuid.uuid4()),
                    certificate="AWS Solutions Architect",
                    certificateAuthority="Amazon Web Services",
                    notExpired=True,
                    issueDate="2023-05-15T00:00:00",
                    expirationDate="2026-05-15T00:00:00",
                    score=None,
                    licenseNo="AWS-SA-001",
                    certificateUrl="https://aws.amazon.com/certification/",
                    foreignLanguage=None,
                    subject="Cloud Architecture",
                    isCTCSponsor=False,
                    grade=None,
                    certificateCatalogId=str(uuid.uuid4()),
                    providerId=str(uuid.uuid4()),
                    provider="Amazon Web Services",
                    fieldId=str(uuid.uuid4()),
                    field="Cloud Computing",
                    subFieldId=str(uuid.uuid4()),
                    subField="Solutions Architecture",
                    levelId=str(uuid.uuid4()),
                    level="Professional",
                    status=0,
                    attendance=True,
                    fileName="aws-certificate.pdf",
                    isSynced=False,
                    isEducation=False,
                    techType="Cloud",
                    rejectReason=None,
                    isNotHasLicenseNumber=False,
                    id=str(uuid.uuid4()),
                    createdOn=datetime.now().isoformat(),
                    createdBy=str(uuid.uuid4()),
                    modifiedOn=datetime.now().isoformat(),
                    modifiedBy=str(uuid.uuid4())
                )
            ],
            languages=[
                LanguageSkill(
                    resumeId=str(uuid.uuid4()),
                    proficiency=90,
                    language=Language(
                        name="English",
                        id=str(uuid.uuid4()),
                        createdOn=datetime.now().isoformat(),
                        createdBy="system",
                        modifiedOn=datetime.now().isoformat(),
                        modifiedBy="system"
                    ),
                    id=str(uuid.uuid4()),
                    createdOn=datetime.now().isoformat(),
                    createdBy="system",
                    modifiedOn=datetime.now().isoformat(),
                    modifiedBy="system"
                )
            ],
            domain=[
                Domain(
                    name="Software Development",
                    year=2023,
                    month=1,
                    resumeId=str(uuid.uuid4()),
                    id=str(uuid.uuid4()),
                    createdOn=datetime.now().isoformat(),
                    createdBy="system",
                    modifiedOn=datetime.now().isoformat(),
                    modifiedBy="system"
                )
            ],
            projects=[
                Project(
                    resumeId=str(uuid.uuid4()),
                    resumeProjectId=str(uuid.uuid4()),
                    projectId=str(uuid.uuid4()),
                    name="E-commerce Platform",
                    projectKey="ECOM-001",
                    projectCode="ECOM-001",
                    projectRank="1",
                    projectLead="John Smith",
                    projectCategory="E-commerce",
                    customerCode="CUST-001",
                    contractType="Fixed Price",
                    url="https://ecom.example.com",
                    company="TechCorp Inc.",
                    type="Web Application",
                    teamSize=10,
                    searchSkill=100,
                    technology=["React", "FastAPI", "PostgreSQL", "Stripe API", "AWS"],
                    projectDescription="Built a full-stack e-commerce platform with 10k+ users using React and Python FastAPI with payment integration",
                    groupname="E-commerce",
                    status="Completed",
                    domain="E-commerce",
                    startDate="2023-01-01",
                    endDate="2023-03-31",
                    painPoins="Performance issues with payment gateway",
                    keyFindings="Optimized API performance",
                    workingProcess="Agile development",
                    responsibility="Full-stack development",
                    technologyByPM="FastAPI",
                    descriptionByPM="Built a robust backend with FastAPI and PostgreSQL",
                    isUpdateTeam=False,
                    applyIncompleted=False,
                    skill="Full-stack development",
                    skillCode="FSD",
                    seniority="Senior",
                    projectRoles=[{"role": "Full-stack Developer", "duration": "3 months"}],
                    projectSkills=[{"skill": "React", "level": "Expert"}],
                    projectJobs=[{"job": "Full-stack Developer", "duration": "3 months"}]
                ),
                Project(
                    resumeId=str(uuid.uuid4()),
                    resumeProjectId=str(uuid.uuid4()),
                    projectId=str(uuid.uuid4()),
                    name="Task Management API",
                    projectKey="TASK-001",
                    projectCode="TASK-001",
                    projectRank="2",
                    projectLead="John Smith",
                    projectCategory="API Development",
                    customerCode="CUST-002",
                    contractType="Time and Material",
                    url="https://api.example.com",
                    company="StartupXYZ",
                    type="API",
                    teamSize=5,
                    searchSkill=80,
                    technology=["Python", "FastAPI", "WebSockets", "Redis", "PostgreSQL"],
                    projectDescription="Developed RESTful API for task management with user authentication and real-time updates serving 1000+ concurrent users",
                    groupname="API",
                    status="Completed",
                    domain="API",
                    startDate="2023-02-01",
                    endDate="2023-03-31",
                    painPoins="Scalability issues with WebSockets",
                    keyFindings="Implemented efficient caching with Redis",
                    workingProcess="Waterfall",
                    responsibility="Backend development",
                    technologyByPM="FastAPI",
                    descriptionByPM="Developed a scalable and efficient API",
                    isUpdateTeam=False,
                    applyIncompleted=False,
                    skill="Backend development",
                    skillCode="BD",
                    seniority="Senior",
                    projectRoles=[{"role": "Backend Developer", "duration": "2 months"}],
                    projectSkills=[{"skill": "FastAPI", "level": "Expert"}],
                    projectJobs=[{"job": "Backend Developer", "duration": "2 months"}]
                )
            ],
            professionalSkills=[
                ProfessionalSkill(
                    id=str(uuid.uuid4()),
                    resumeId=str(uuid.uuid4()),
                    jobTitleName="Senior Software Engineer",
                    experienceMonth=60,
                    experienceYear=5,
                    jobFillByUser="John Smith",
                    isMainSkill=True,
                    projectInfo=[
                        {"projectId": str(uuid.uuid4()), "duration": "2 months"},
                        {"projectId": str(uuid.uuid4()), "duration": "3 months"}
                    ]
                )
            ]
        ),
        
        Resume(
            name="Sarah Johnson",
            email="sarah.johnson@email.com",
            phone="+1-555-0124",
            summary="Data Scientist with 4+ years of experience in machine learning, statistical analysis, and data visualization. Built ML models with 95%+ accuracy and reduced business costs by 30%.",
            education=Education(
                resumeId=str(uuid.uuid4()),
                school="Tech University",
                degree="Master of Science in Data Science",
                major="Data Science",
                start="2020-09-01",
                end="2022-05-15",
                grade="3.9/4.0",
                completeDegree=True,
                id=str(uuid.uuid4()),
                createdOn=datetime.now().isoformat(),
                createdBy="system",
                modifiedOn=datetime.now().isoformat(),
                modifiedBy="system"
            ),
            certificates=[
                Certificate(
                    resumeId=str(uuid.uuid4()),
                    certificate="TensorFlow Developer Certificate",
                    certificateAuthority="Google",
                    notExpired=True,
                    issueDate="2022-05-15T00:00:00",
                    expirationDate="2025-05-15T00:00:00",
                    score=None,
                    licenseNo="TF-DEV-002",
                    certificateUrl="https://www.tensorflow.org/certificate",
                    foreignLanguage=None,
                    subject="Machine Learning",
                    isCTCSponsor=False,
                    grade=None,
                    certificateCatalogId=str(uuid.uuid4()),
                    providerId=str(uuid.uuid4()),
                    provider="Google",
                    fieldId=str(uuid.uuid4()),
                    field="Machine Learning",
                    subFieldId=str(uuid.uuid4()),
                    subField="Deep Learning",
                    levelId=str(uuid.uuid4()),
                    level="Professional",
                    status=0,
                    attendance=True,
                    fileName="tensorflow-certificate.pdf",
                    isSynced=False,
                    isEducation=False,
                    techType="ML",
                    rejectReason=None,
                    isNotHasLicenseNumber=False,
                    id=str(uuid.uuid4()),
                    createdOn=datetime.now().isoformat(),
                    createdBy=str(uuid.uuid4()),
                    modifiedOn=datetime.now().isoformat(),
                    modifiedBy=str(uuid.uuid4())
                )
            ],
            languages=[
                LanguageSkill(
                    resumeId=str(uuid.uuid4()),
                    proficiency=95,
                    language=Language(
                        name="English",
                        id=str(uuid.uuid4()),
                        createdOn=datetime.now().isoformat(),
                        createdBy="system",
                        modifiedOn=datetime.now().isoformat(),
                        modifiedBy="system"
                    ),
                    id=str(uuid.uuid4()),
                    createdOn=datetime.now().isoformat(),
                    createdBy="system",
                    modifiedOn=datetime.now().isoformat(),
                    modifiedBy="system"
                )
            ],
            domain=[
                Domain(
                    name="Data Science",
                    year=2023,
                    month=1,
                    resumeId=str(uuid.uuid4()),
                    id=str(uuid.uuid4()),
                    createdOn=datetime.now().isoformat(),
                    createdBy="system",
                    modifiedOn=datetime.now().isoformat(),
                    modifiedBy="system"
                )
            ],
            projects=[
                Project(
                    resumeId=str(uuid.uuid4()),
                    resumeProjectId=str(uuid.uuid4()),
                    projectId=str(uuid.uuid4()),
                    name="Customer Churn Prediction",
                    projectKey="ML-001",
                    projectCode="ML-001",
                    projectRank="1",
                    projectLead="Sarah Johnson",
                    projectCategory="Machine Learning",
                    customerCode="CUST-003",
                    contractType="Fixed Price",
                    url="https://ml.example.com",
                    company="DataTech Solutions",
                    type="ML Model",
                    teamSize=4,
                    searchSkill=90,
                    technology=["Python", "Scikit-learn", "XGBoost", "Pandas", "AWS SageMaker"],
                    projectDescription="Built ML model to predict customer churn with 92% accuracy using ensemble methods, saving company $2M annually",
                    groupname="ML",
                    status="Completed",
                    domain="ML",
                    startDate="2023-01-01",
                    endDate="2023-03-31",
                    painPoins="Overfitting issues with ensemble methods",
                    keyFindings="Optimized model performance",
                    workingProcess="Agile",
                    responsibility="ML Model Development",
                    technologyByPM="Scikit-learn",
                    descriptionByPM="Developed a robust ML model for churn prediction",
                    isUpdateTeam=False,
                    applyIncompleted=False,
                    skill="ML Model Development",
                    skillCode="MLD",
                    seniority="Senior",
                    projectRoles=[{"role": "Data Scientist", "duration": "4 months"}],
                    projectSkills=[{"skill": "Scikit-learn", "level": "Expert"}],
                    projectJobs=[{"job": "Data Scientist", "duration": "4 months"}]
                ),
                Project(
                    resumeId=str(uuid.uuid4()),
                    resumeProjectId=str(uuid.uuid4()),
                    projectId=str(uuid.uuid4()),
                    name="Real-time Fraud Detection",
                    projectKey="ML-002",
                    projectCode="ML-002",
                    projectRank="2",
                    projectLead="Sarah Johnson",
                    projectCategory="Machine Learning",
                    customerCode="CUST-004",
                    contractType="Time and Material",
                    url="https://fraud.example.com",
                    company="DataTech Solutions",
                    type="ML Model",
                    teamSize=6,
                    searchSkill=95,
                    technology=["Python", "Apache Kafka", "TensorFlow", "Redis", "Kubernetes"],
                    projectDescription="Implemented real-time fraud detection system using streaming data and anomaly detection, reducing fraud by 45%",
                    groupname="ML",
                    status="Completed",
                    domain="ML",
                    startDate="2023-02-01",
                    endDate="2023-03-31",
                    painPoins="Scalability issues with Kafka",
                    keyFindings="Optimized anomaly detection",
                    workingProcess="Waterfall",
                    responsibility="ML Model Development",
                    technologyByPM="TensorFlow",
                    descriptionByPM="Developed a scalable fraud detection system",
                    isUpdateTeam=False,
                    applyIncompleted=False,
                    skill="ML Model Development",
                    skillCode="MLD",
                    seniority="Senior",
                    projectRoles=[{"role": "Data Scientist", "duration": "6 months"}],
                    projectSkills=[{"skill": "TensorFlow", "level": "Expert"}],
                    projectJobs=[{"job": "Data Scientist", "duration": "6 months"}]
                )
            ],
            professionalSkills=[
                ProfessionalSkill(
                    id=str(uuid.uuid4()),
                    resumeId=str(uuid.uuid4()),
                    jobTitleName="Senior Data Scientist",
                    experienceMonth=48,
                    experienceYear=4,
                    jobFillByUser="Sarah Johnson",
                    isMainSkill=True,
                    projectInfo=[
                        {"projectId": str(uuid.uuid4()), "duration": "2 months"},
                        {"projectId": str(uuid.uuid4()), "duration": "2 months"}
                    ]
                )
            ]
        ),
        
        Resume(
            name="Alex Chen",
            email="alex.chen@email.com",
            phone="+1-555-0125",
            summary="Full-stack Developer with 3+ years of experience in modern web technologies. Specialized in React, Node.js, and cloud infrastructure with focus on performance optimization.",
            education=Education(
                resumeId=str(uuid.uuid4()),
                school="Tech Institute",
                degree="Bachelor of Science in Software Engineering",
                major="Software Engineering",
                start="2021-09-01",
                end="2023-05-15",
                grade="3.6/4.0",
                completeDegree=True,
                id=str(uuid.uuid4()),
                createdOn=datetime.now().isoformat(),
                createdBy="system",
                modifiedOn=datetime.now().isoformat(),
                modifiedBy="system"
            ),
            certificates=[
                Certificate(
                    resumeId=str(uuid.uuid4()),
                    certificate="React Developer Certification",
                    certificateAuthority="Meta",
                    notExpired=True,
                    issueDate="2023-05-15T00:00:00",
                    expirationDate="2026-05-15T00:00:00",
                    score=None,
                    licenseNo="REACT-DEV-003",
                    certificateUrl="https://www.coursera.org/professional-certificates/meta-react-native",
                    foreignLanguage=None,
                    subject="Frontend Development",
                    isCTCSponsor=False,
                    grade=None,
                    certificateCatalogId=str(uuid.uuid4()),
                    providerId=str(uuid.uuid4()),
                    provider="Meta",
                    fieldId=str(uuid.uuid4()),
                    field="Web Development",
                    subFieldId=str(uuid.uuid4()),
                    subField="Frontend Development",
                    levelId=str(uuid.uuid4()),
                    level="Professional",
                    status=0,
                    attendance=True,
                    fileName="react-certificate.pdf",
                    isSynced=False,
                    isEducation=False,
                    techType="Web",
                    rejectReason=None,
                    isNotHasLicenseNumber=False,
                    id=str(uuid.uuid4()),
                    createdOn=datetime.now().isoformat(),
                    createdBy=str(uuid.uuid4()),
                    modifiedOn=datetime.now().isoformat(),
                    modifiedBy=str(uuid.uuid4())
                )
            ],
            languages=[
                LanguageSkill(
                    resumeId=str(uuid.uuid4()),
                    proficiency=98,
                    language=Language(
                        name="English",
                        id=str(uuid.uuid4()),
                        createdOn=datetime.now().isoformat(),
                        createdBy="system",
                        modifiedOn=datetime.now().isoformat(),
                        modifiedBy="system"
                    ),
                    id=str(uuid.uuid4()),
                    createdOn=datetime.now().isoformat(),
                    createdBy="system",
                    modifiedOn=datetime.now().isoformat(),
                    modifiedBy="system"
                )
            ],
            domain=[
                Domain(
                    name="Full-stack Development",
                    year=2023,
                    month=1,
                    resumeId=str(uuid.uuid4()),
                    id=str(uuid.uuid4()),
                    createdOn=datetime.now().isoformat(),
                    createdBy="system",
                    modifiedOn=datetime.now().isoformat(),
                    modifiedBy="system"
                )
            ],
            projects=[
                Project(
                    resumeId=str(uuid.uuid4()),
                    resumeProjectId=str(uuid.uuid4()),
                    projectId=str(uuid.uuid4()),
                    name="Social Media Dashboard",
                    projectKey="WEB-001",
                    projectCode="WEB-001",
                    projectRank="1",
                    projectLead="Alex Chen",
                    projectCategory="Web Development",
                    customerCode="CUST-005",
                    contractType="Fixed Price",
                    url="https://dashboard.example.com",
                    company="WebTech Solutions",
                    type="Web Application",
                    teamSize=5,
                    searchSkill=100,
                    technology=["React", "Node.js", "MongoDB", "Chart.js", "AWS"],
                    projectDescription="Built comprehensive social media analytics dashboard with real-time data visualization for 500+ users",
                    groupname="Web",
                    status="Completed",
                    domain="Web",
                    startDate="2023-01-01",
                    endDate="2023-05-15",
                    painPoins="Performance issues with Chart.js",
                    keyFindings="Optimized data fetching",
                    workingProcess="Agile",
                    responsibility="Full-stack development",
                    technologyByPM="React",
                    descriptionByPM="Built a responsive and performant dashboard",
                    isUpdateTeam=False,
                    applyIncompleted=False,
                    skill="Full-stack development",
                    skillCode="FSD",
                    seniority="Senior",
                    projectRoles=[{"role": "Full-stack Developer", "duration": "5 months"}],
                    projectSkills=[{"skill": "React", "level": "Expert"}],
                    projectJobs=[{"job": "Full-stack Developer", "duration": "5 months"}]
                ),
                Project(
                    resumeId=str(uuid.uuid4()),
                    resumeProjectId=str(uuid.uuid4()),
                    projectId=str(uuid.uuid4()),
                    name="E-learning Platform",
                    projectKey="WEB-002",
                    projectCode="WEB-002",
                    projectRank="2",
                    projectLead="Alex Chen",
                    projectCategory="Web Development",
                    customerCode="CUST-006",
                    contractType="Time and Material",
                    url="https://learn.example.com",
                    company="DesignCorp",
                    type="Web Application",
                    teamSize=8,
                    searchSkill=100,
                    technology=["React", "Node.js", "Express", "MongoDB", "Socket.io"],
                    projectDescription="Developed online learning platform with video streaming and interactive features serving 2000+ students",
                    groupname="Web",
                    status="Completed",
                    domain="Web",
                    startDate="2023-02-01",
                    endDate="2023-05-15",
                    painPoins="Scalability issues with Socket.io",
                    keyFindings="Optimized video streaming",
                    workingProcess="Waterfall",
                    responsibility="Full-stack development",
                    technologyByPM="React",
                    descriptionByPM="Developed a scalable and interactive learning platform",
                    isUpdateTeam=False,
                    applyIncompleted=False,
                    skill="Full-stack development",
                    skillCode="FSD",
                    seniority="Senior",
                    projectRoles=[{"role": "Full-stack Developer", "duration": "8 months"}],
                    projectSkills=[{"skill": "React", "level": "Expert"}],
                    projectJobs=[{"job": "Full-stack Developer", "duration": "8 months"}]
                )
            ],
            professionalSkills=[
                ProfessionalSkill(
                    id=str(uuid.uuid4()),
                    resumeId=str(uuid.uuid4()),
                    jobTitleName="Full-stack Developer",
                    experienceMonth=36,
                    experienceYear=3,
                    jobFillByUser="Alex Chen",
                    isMainSkill=True,
                    projectInfo=[
                        {"projectId": str(uuid.uuid4()), "duration": "5 months"},
                        {"projectId": str(uuid.uuid4()), "duration": "8 months"}
                    ]
                )
            ]
        )
    ]
    
    return resumes

def generate_sample_job_descriptions() -> List[JobDescription]:
    """Generate sample job descriptions for different roles with enhanced requirements."""
    
    job_descriptions = [
        JobDescription(
            title="Senior Software Engineer",
            company="InnovateTech Corp",
            department="Engineering",
            level="Senior",
            requirements=[
                "Bachelor's degree in Computer Science or related field",
                "5+ years of software development experience",
                "Strong proficiency in Python and JavaScript",
                "Experience with cloud platforms (AWS, Azure, or GCP)",
                "Knowledge of microservices architecture",
                "Experience with database design and optimization",
                "Strong problem-solving and communication skills"
            ],
            responsibilities=[
                "Design and develop scalable web applications",
                "Lead technical discussions and code reviews",
                "Mentor junior developers",
                "Collaborate with product managers and designers",
                "Implement best practices for code quality and testing",
                "Optimize application performance and scalability",
                "Participate in system architecture decisions"
            ],
            skills_required=["Python", "JavaScript", "React", "FastAPI", "PostgreSQL", "AWS", "Docker", "Git", "REST APIs"],
            experience_years="5-8 years"
        ),
        
        JobDescription(
            title="Data Scientist",
            company="AI Innovations Ltd",
            department="Data Science",
            level="Mid-Senior",
            requirements=[
                "Master's degree in Data Science, Statistics, or related field",
                "3+ years of experience in data science and machine learning",
                "Strong programming skills in Python and R",
                "Experience with deep learning frameworks",
                "Knowledge of statistical modeling and analysis",
                "Experience with big data technologies",
                "Strong analytical and problem-solving skills"
            ],
            responsibilities=[
                "Develop machine learning models for business problems",
                "Analyze large datasets to extract insights",
                "Create data visualizations and reports",
                "Collaborate with engineering teams on model deployment",
                "Stay current with latest ML/AI research and techniques",
                "Design and conduct A/B tests",
                "Communicate findings to stakeholders"
            ],
            skills_required=["Python", "R", "TensorFlow", "PyTorch", "SQL", "Tableau", "Apache Spark", "AWS", "Statistics"],
            experience_years="3-6 years"
        ),
        
        JobDescription(
            title="Full-stack Developer", 
            company="StartupHub Inc",
            department="Product Development",
            level="Mid-level",
            requirements=[
                "Bachelor's degree in Computer Science or related field",
                "3+ years of full-stack development experience",
                "Proficiency in JavaScript/TypeScript and modern frameworks",
                "Experience with both SQL and NoSQL databases",
                "Knowledge of RESTful API design",
                "Experience with cloud deployment",
                "Understanding of agile development methodologies"
            ],
            responsibilities=[
                "Develop end-to-end web applications",
                "Build responsive user interfaces",
                "Design and implement RESTful APIs",
                "Optimize application performance",
                "Write comprehensive tests",
                "Collaborate with cross-functional teams",
                "Participate in code reviews and technical discussions"
            ],
            skills_required=["JavaScript", "TypeScript", "React", "Node.js", "MongoDB", "PostgreSQL", "AWS", "GraphQL"],
            experience_years="3-5 years"
        )
    ]
    
    return job_descriptions

def generate_question_banks() -> List[QuestionBank]:
    """Generate comprehensive question banks for different categories and difficulty levels."""
    
    question_banks = [
        QuestionBank(
            category="Technical - Software Engineering",
            difficulty="Medium",
            questions=[
                {
                    "question": "Explain the difference between SQL and NoSQL databases. When would you choose one over the other?",
                    "follow_up": "Can you give me a specific example from your experience where you chose one type and why?"
                },
                {
                    "question": "How do you handle error handling and logging in your applications?",
                    "follow_up": "What specific logging frameworks or tools have you used?"
                },
                {
                    "question": "Describe your experience with API design. What makes a good RESTful API?",
                    "follow_up": "How do you handle API versioning and backward compatibility?"
                },
                {
                    "question": "Explain how you would optimize a slow-performing database query.",
                    "follow_up": "What tools do you use to monitor and debug database performance?"
                },
                {
                    "question": "How do you ensure code quality in your development process?",
                    "follow_up": "What testing strategies do you implement?"
                },
                {
                    "question": "Describe your experience with microservices architecture.",
                    "follow_up": "What challenges have you faced when implementing microservices?"
                }
            ]
        ),
        
        QuestionBank(
            category="Technical - Data Science",
            difficulty="Medium",
            questions=[
                {
                    "question": "Explain the bias-variance tradeoff in machine learning.",
                    "follow_up": "How do you detect and handle overfitting in your models?"
                },
                {
                    "question": "How do you handle missing data in your datasets?",
                    "follow_up": "What's your experience with different imputation techniques?"
                },
                {
                    "question": "Describe your approach to feature engineering.",
                    "follow_up": "Can you give an example of a creative feature you've engineered that improved model performance?"
                },
                {
                    "question": "How do you evaluate the performance of a classification model?",
                    "follow_up": "When would you use precision vs recall as your primary metric?"
                },
                {
                    "question": "Explain the difference between supervised and unsupervised learning.",
                    "follow_up": "Can you describe a project where you used unsupervised learning?"
                },
                {
                    "question": "How do you ensure your machine learning models are production-ready?",
                    "follow_up": "What monitoring strategies do you implement for deployed models?"
                }
            ]
        ),
        
        QuestionBank(
            category="Behavioral",
            difficulty="General",
            questions=[
                {
                    "question": "Tell me about a challenging project you worked on. What made it challenging and how did you overcome the obstacles?",
                    "follow_up": "What would you do differently if you had to do it again?"
                },
                {
                    "question": "Describe a time when you had to work with a difficult team member. How did you handle the situation?",
                    "follow_up": "What did you learn from that experience about team dynamics?"
                },
                {
                    "question": "Tell me about a time when you had to learn a new technology quickly for a project.",
                    "follow_up": "How do you typically approach learning new technologies or frameworks?"
                },
                {
                    "question": "Describe a situation where you had to make a decision with incomplete information.",
                    "follow_up": "How do you typically handle uncertainty in your work?"
                },
                {
                    "question": "Tell me about a time when you disagreed with your manager or team lead about a technical decision.",
                    "follow_up": "How do you handle technical disagreements in general?"
                },
                {
                    "question": "Describe a time when you had to mentor or help a junior colleague.",
                    "follow_up": "What strategies do you use to effectively share knowledge?"
                }
            ]
        ),
        
        QuestionBank(
            category="Project Deep Dive",
            difficulty="General",
            questions=[
                {
                    "question": "Walk me through your most challenging project from start to finish.",
                    "follow_up": "What technologies did you choose and what influenced those decisions?"
                },
                {
                    "question": "How did you handle testing in this project?",
                    "follow_up": "What was your test coverage strategy and how did you measure quality?"
                },
                {
                    "question": "What was the most difficult technical decision you had to make in this project?",
                    "follow_up": "How did you evaluate the alternatives before making the decision?"
                },
                {
                    "question": "How did you ensure the scalability and performance of your solution?",
                    "follow_up": "What specific metrics did you use to monitor performance?"
                },
                {
                    "question": "Describe how you collaborated with other team members on this project.",
                    "follow_up": "What tools or processes did you use for collaboration?"
                },
                {
                    "question": "What was the biggest lesson you learned from this project?",
                    "follow_up": "How has this experience influenced your approach to new projects?"
                }
            ]
        )
    ]
    
    return question_banks

def setup_database_if_available():
    """Setup PostgreSQL database tables if connection is available."""
    try:
        from rag_system import InterviewRAG
        
        # Try to initialize RAG system (which includes database setup)
        rag = InterviewRAG()
        if rag.engine:
            logger.info("PostgreSQL database initialized successfully")
            return True
        else:
            logger.info("PostgreSQL not available, continuing with file-based storage only")
            return False
            
    except Exception as e:
        logger.warning(f"Database setup failed: {e}")
        return False

def save_mock_data():
    """Save all mock data to JSON files and optionally initialize database."""
    
    logger.info("Generating mock data for interview system...")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Generate and save resumes
    resumes = generate_sample_resumes()
    with open("data/resumes.json", "w") as f:
        json.dump([asdict(resume) for resume in resumes], f, indent=2)
    
    # Generate and save job descriptions
    job_descriptions = generate_sample_job_descriptions()
    with open("data/job_descriptions.json", "w") as f:
        json.dump([asdict(job_desc) for job_desc in job_descriptions], f, indent=2)
    
    # Generate and save question banks
    question_banks = generate_question_banks()
    with open("data/question_banks.json", "w") as f:
        json.dump([asdict(qbank) for qbank in question_banks], f, indent=2)
    
    print("Mock data generated successfully!")
    print(f"- {len(resumes)} resumes saved to data/resumes.json")
    print(f"- {len(job_descriptions)} job descriptions saved to data/job_descriptions.json")
    print(f"- {len(question_banks)} question banks saved to data/question_banks.json")
    
    # Try to setup database
    db_available = setup_database_if_available()
    if db_available:
        print("- PostgreSQL database tables initialized")
    else:
        print("- PostgreSQL not available, using file-based storage only")
    
    print("\nData is ready for the interview agent!")

def clean_data():
    """Clean up generated data files."""
    files_to_clean = [
        "data/resumes.json",
        "data/job_descriptions.json", 
        "data/question_banks.json"
    ]
    
    for file_path in files_to_clean:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed {file_path}")
    
    if os.path.exists("data") and not os.listdir("data"):
        os.rmdir("data")
        print("Removed empty data directory")

if __name__ == "__main__":
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean_data()
    else:
        save_mock_data() 