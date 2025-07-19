"""
RAG system for interview agent using ChromaDB vector database and PostgreSQL for persistence.
Handles storage and retrieval of resumes, job descriptions, and question banks.
"""

import json
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
import uuid

load_dotenv()
logger = logging.getLogger(__name__)

# Database Models
Base = declarative_base()

class InterviewSession(Base):
    """Database model for interview sessions."""
    __tablename__ = "interview_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interview_id = Column(String(255), unique=True, nullable=False)
    candidate_name = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    status = Column(String(50), default="in_progress")  # in_progress, completed, cancelled
    
    # Interview data (stored as JSON for flexibility)
    resume_content = Column(Text)
    job_description = Column(Text)
    interview_plan = Column(JSON)
    questions_and_answers = Column(JSON)
    interview_summary = Column(JSON)
    transcription = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class InterviewMetrics(Base):
    """Database model for interview metrics and analytics."""
    __tablename__ = "interview_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interview_id = Column(String(255), nullable=False)
    
    # Performance metrics
    total_questions = Column(Integer)
    questions_answered = Column(Integer)
    follow_up_questions = Column(Integer)
    total_duration_minutes = Column(Float)
    
    # Answer quality scores
    avg_completeness_score = Column(Float)
    avg_clarity_score = Column(Float)
    avg_technical_depth_score = Column(Float)
    avg_relevance_score = Column(Float)
    
    # Token usage
    total_tokens_used = Column(Integer)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class InterviewRAG:
    """Enhanced RAG system for interview-related data with PostgreSQL integration."""
    
    def __init__(self, persist_directory: str = "./chroma_db", postgres_url: Optional[str] = None):
        """Initialize the RAG system with ChromaDB and PostgreSQL."""
        self.persist_directory = persist_directory
        
        # Use more efficient embedding model for token efficiency
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            dimensions=1536  # Reduced dimensions for efficiency
        )
        
        # Initialize ChromaDB client with optimized settings
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Create collections for different data types with optimized settings
        self.resumes_collection = self.client.get_or_create_collection(
            name="resumes"
        )
        
        self.job_descriptions_collection = self.client.get_or_create_collection(
            name="job_descriptions"
        )
        
        self.questions_collection = self.client.get_or_create_collection(
            name="questions"
        )
        
        # Optimized text splitter for better chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,  # Reduced for token efficiency
            chunk_overlap=100,  # Reduced overlap
            length_function=len,
            separators=["\n\n", "\n", ". ", ".", " ", ""]
        )
        
        # PostgreSQL setup
        self.postgres_url = postgres_url or os.getenv("DATABASE_URL", "postgresql://sangh:123qwe123@localhost:5432/interview_db")
        self.engine = None
        self.SessionLocal = None
        self._setup_database()
        
    def _setup_database(self):
        """Setup PostgreSQL database connection and create tables."""
        try:
            self.engine = create_engine(self.postgres_url, echo=False)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # Create tables
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database connection established and tables created")
        except Exception as e:
            logger.warning(f"PostgreSQL connection failed: {e}. Continuing without database persistence.")
            self.engine = None
            self.SessionLocal = None
    
    def get_db_session(self) -> Optional[Session]:
        """Get database session if available."""
        if self.SessionLocal:
            return self.SessionLocal()
        return None
    
    def _format_resume_text(self, resume: Dict[str, Any]) -> str:
        """Format resume data into searchable text with token efficiency."""
        # Concise formatting to reduce token usage
        parts = [
            f"{resume['name']} | {resume.get('email', '')}",
            f"Summary: {resume['summary'][:200]}..." if len(resume['summary']) > 200 else f"Summary: {resume['summary']}"
        ]
        
        # Add education information
        if resume.get('education'):
            edu = resume['education']
            parts.append(f"Education: {edu.get('degree', '')} in {edu.get('major', '')} from {edu.get('school', '')}")
        
        # Add professional skills (limit to top skills)
        if resume.get('professionalSkills'):
            skill_names = [skill.get('jobTitleName', '') for skill in resume['professionalSkills'][:5]]
            if skill_names:
                parts.append(f"Skills: {', '.join(filter(None, skill_names))}")
        
        # Fallback to legacy skills if present (for backward compatibility)
        elif resume.get('skills'):
            parts.append(f"Skills: {', '.join(resume['skills'][:10])}")
        
        # Add domain experience
        if resume.get('domain'):
            domains = [dom.get('name', '') for dom in resume['domain'][:3]]
            if domains:
                parts.append(f"Domains: {', '.join(filter(None, domains))}")
        
        # Add key projects (limit to 2)
        if resume.get('projects'):
            for project in resume['projects'][:2]:
                proj_name = project.get('name', '')
                proj_desc = project.get('projectDescription', '')
                if proj_name and proj_desc:
                    parts.append(f"Project: {proj_name} - {proj_desc[:100]}...")
        
        # Add key experience (legacy format for backward compatibility)
        if resume.get('experience'):
            for exp in resume['experience'][:2]:
                if isinstance(exp, dict):
                    parts.append(f"{exp.get('title', '')} at {exp.get('company', '')} - {exp.get('description', '')[:150]}...")
        
        # Add certificates (limit to 2 most relevant)
        if resume.get('certificates'):
            for cert in resume['certificates'][:2]:
                cert_name = cert.get('certificate', '')
                cert_auth = cert.get('certificateAuthority', '')
                if cert_name:
                    parts.append(f"Certificate: {cert_name} from {cert_auth}")
        
        # Add languages
        if resume.get('languages'):
            languages = []
            for lang in resume['languages'][:3]:
                if isinstance(lang.get('language'), dict):
                    lang_name = lang['language'].get('name', '')
                    proficiency = lang.get('proficiency', 0)
                    if lang_name:
                        languages.append(f"{lang_name} ({proficiency}%)")
            if languages:
                parts.append(f"Languages: {', '.join(languages)}")
        
        return "\n".join(filter(None, parts))
    
    def _format_job_description_text(self, job_desc: Dict[str, Any]) -> str:
        """Format job description into searchable text with token efficiency."""
        parts = [
            f"{job_desc['title']} at {job_desc['company']}",
            f"Level: {job_desc['level']} | Experience: {job_desc['experience_years']}",
            f"Skills: {', '.join(job_desc['skills_required'][:8])}",  # Limit skills
            f"Requirements: {'; '.join(job_desc['requirements'][:3])}"  # Limit requirements
        ]
        
        return "\n".join(parts)
    
    def _format_question_text(self, question_data: Dict[str, Any]) -> str:
        """Format question data into searchable text."""
        return f"{question_data['category']} | {question_data['difficulty']} | {question_data['question']}"
    
    def load_data_from_files(self):
        """Load mock data from JSON files into the vector database."""
        logger.info("Loading data into vector database...")
        
        # Load resumes
        if os.path.exists("data/resumes.json"):
            with open("data/resumes.json", "r") as f:
                resumes = json.load(f)
            
            # Clear existing resumes
            # if self.resumes_collection.count() > 0:
            #     self.resumes_collection.
            
            # Add resumes to collection with batch processing for efficiency
            documents = []
            metadatas = []
            ids = []
            
            for i, resume in enumerate(resumes):
                resume_text = self._format_resume_text(resume)
                documents.append(resume_text)
                
                # Extract skills from new structure or fallback to legacy
                skills = []
                if resume.get('professionalSkills'):
                    skills = [skill.get('jobTitleName', '') for skill in resume['professionalSkills'][:5]]
                elif resume.get('skills'):
                    skills = resume['skills'][:5]
                
                # Count experience from projects or legacy experience
                experience_count = 0
                if resume.get('projects'):
                    experience_count = len(resume['projects'])
                elif resume.get('experience'):
                    experience_count = len(resume['experience'])
                
                metadatas.append({
                    "type": "resume",
                    "name": resume['name'],
                    "skills": json.dumps(list(filter(None, skills))),  # Limit metadata size
                    "experience_count": experience_count,
                    "education": resume.get('education', {}).get('degree', '') if resume.get('education') else '',
                    "domain_count": len(resume.get('domain', []))
                })
                ids.append(f"resume_{i}")
            
            # Batch add for efficiency
            embeddings = self.embeddings.embed_documents(documents)
            self.resumes_collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Loaded {len(resumes)} resumes")
        
        # Load job descriptions
        if os.path.exists("data/job_descriptions.json"):
            with open("data/job_descriptions.json", "r") as f:
                job_descriptions = json.load(f)
            
            # Clear existing job descriptions
            # if self.job_descriptions_collection.count() > 0:
            #     self.job_descriptions_collection.delete(where={})
            
            documents = []
            metadatas = []
            ids = []
            
            for i, job_desc in enumerate(job_descriptions):
                job_text = self._format_job_description_text(job_desc)
                documents.append(job_text)
                metadatas.append({
                    "type": "job_description",
                    "title": job_desc['title'],
                    "company": job_desc['company'],
                    "level": job_desc['level']
                })
                ids.append(f"job_{i}")
            
            # Batch add for efficiency
            embeddings = self.embeddings.embed_documents(documents)
            self.job_descriptions_collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Loaded {len(job_descriptions)} job descriptions")
        
        # Load questions
        if os.path.exists("data/question_banks.json"):
            with open("data/question_banks.json", "r") as f:
                question_banks = json.load(f)
            
            # Clear existing questions
            # if self.questions_collection.count() > 0:
            #     self.questions_collection.delete(where={})
            
            documents = []
            metadatas = []
            ids = []
            question_id = 0
            
            for bank in question_banks:
                for question in bank['questions']:
                    question_data = {
                        "category": bank['category'],
                        "difficulty": bank['difficulty'],
                        "question": question['question'],
                        "follow_up": question.get('follow_up', '')
                    }
                    
                    question_text = self._format_question_text(question_data)
                    documents.append(question_text)
                    metadatas.append({
                        "type": "question",
                        "category": bank['category'],
                        "difficulty": bank['difficulty'],
                        "question": question['question'][:200],  # Truncate for metadata
                        "follow_up": question.get('follow_up', '')[:100]  # Truncate for metadata
                    })
                    ids.append(f"question_{question_id}")
                    question_id += 1
            
            # Batch add for efficiency
            embeddings = self.embeddings.embed_documents(documents)
            self.questions_collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Loaded {question_id} questions")
        
        logger.info("Data loading completed successfully!")
    
    def search_resumes(self, query: str, n_results: int = 2) -> List[Dict[str, Any]]:
        """Search for relevant resumes with optimized retrieval."""
        embedding = self.embeddings.embed_query(query)
        
        results = self.resumes_collection.query(
            query_embeddings=[embedding],
            n_results=min(n_results, 3)  # Limit results for efficiency
        )
        
        return [
            {
                "content": doc,
                "metadata": meta,
                "score": 1 - distance
            }
            for doc, meta, distance in zip(
                results['documents'][0],
                results['metadatas'][0], 
                results['distances'][0]
            ) if (1 - distance) > 0.7  # Filter low-quality results
        ]
    
    def search_job_descriptions(self, query: str, n_results: int = 2) -> List[Dict[str, Any]]:
        """Search for relevant job descriptions with optimized retrieval."""
        embedding = self.embeddings.embed_query(query)
        
        results = self.job_descriptions_collection.query(
            query_embeddings=[embedding],
            n_results=min(n_results, 3)
        )
        
        return [
            {
                "content": doc,
                "metadata": meta,
                "score": 1 - distance
            }
            for doc, meta, distance in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            ) if (1 - distance) > 0.7
        ]
    
    def search_questions(self, query: str, category: Optional[str] = None, n_results: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant questions with optimized retrieval."""
        embedding = self.embeddings.embed_query(query)
        
        where_filter = {}
        if category:
            where_filter["category"] = category
        
        results = self.questions_collection.query(
            query_embeddings=[embedding],
            n_results=min(n_results, 5),
            where=where_filter if where_filter else None
        )
        
        return [
            {
                "content": doc,
                "metadata": meta,
                "score": 1 - distance
            }
            for doc, meta, distance in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            ) if (1 - distance) > 0.6  # Slightly lower threshold for questions
        ]
    
    def get_questions_by_category(self, category: str, n_results: int = 6) -> List[Dict[str, Any]]:
        """Get questions filtered by category with limit."""
        results = self.questions_collection.get(
            where={"category": category},
            limit=min(n_results, 8)  # Limit for efficiency
        )
        
        return [
            {
                "content": doc,
                "metadata": meta
            }
            for doc, meta in zip(results['documents'], results['metadatas'])
        ]
    
    def save_interview_session(self, interview_data: Dict[str, Any]) -> Optional[str]:
        """Save interview session to PostgreSQL."""
        db = self.get_db_session()
        if not db:
            logger.warning("Database not available. Skipping interview save.")
            return None
        
        try:
            session = InterviewSession(
                interview_id=interview_data.get("interview_id"),
                candidate_name=interview_data.get("candidate_name"),
                start_time=interview_data.get("start_time"),
                end_time=interview_data.get("end_time"),
                status=interview_data.get("status", "completed"),
                resume_content=interview_data.get("resume_content"),
                job_description=interview_data.get("job_description"),
                interview_plan=interview_data.get("interview_plan"),
                questions_and_answers=interview_data.get("questions_and_answers"),
                interview_summary=interview_data.get("interview_summary"),
                transcription=interview_data.get("transcription")
            )
            
            db.add(session)
            db.commit()
            db.refresh(session)
            
            logger.info(f"Interview session saved with ID: {session.id}")
            return str(session.id)
            
        except Exception as e:
            logger.error(f"Failed to save interview session: {e}")
            db.rollback()
            return None
        finally:
            db.close()
    
    def save_interview_metrics(self, interview_id: str, metrics: Dict[str, Any]) -> Optional[str]:
        """Save interview metrics to PostgreSQL."""
        db = self.get_db_session()
        if not db:
            return None
        
        try:
            metrics_record = InterviewMetrics(
                interview_id=interview_id,
                total_questions=metrics.get("total_questions"),
                questions_answered=metrics.get("questions_answered"),
                follow_up_questions=metrics.get("follow_up_questions"),
                total_duration_minutes=metrics.get("total_duration_minutes"),
                avg_completeness_score=metrics.get("avg_completeness_score"),
                avg_clarity_score=metrics.get("avg_clarity_score"),
                avg_technical_depth_score=metrics.get("avg_technical_depth_score"),
                avg_relevance_score=metrics.get("avg_relevance_score"),
                total_tokens_used=metrics.get("total_tokens_used"),
                prompt_tokens=metrics.get("prompt_tokens"),
                completion_tokens=metrics.get("completion_tokens")
            )
            
            db.add(metrics_record)
            db.commit()
            db.refresh(metrics_record)
            
            return str(metrics_record.id)
            
        except Exception as e:
            logger.error(f"Failed to save interview metrics: {e}")
            db.rollback()
            return None
        finally:
            db.close()

def initialize_rag_system() -> InterviewRAG:
    """Initialize and populate the RAG system."""
    rag = InterviewRAG()
    
    # Check if data files exist, if not generate them
    if not os.path.exists("data"):
        logger.info("Data directory not found. Generating mock data...")
        from mock_data_generator import save_mock_data
        save_mock_data()
    
    # Load data into vector database
    rag.load_data_from_files()
    
    return rag

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize RAG system
    rag = initialize_rag_system()
    
    # Test searches
    print("\n=== Testing Resume Search ===")
    resume_results = rag.search_resumes("Python software engineer with API experience")
    for result in resume_results:
        print(f"Score: {result['score']:.3f}")
        print(f"Name: {result['metadata']['name']}")
        print(f"Content preview: {result['content'][:200]}...")
        print()
    
    print("\n=== Testing Job Search ===")
    job_results = rag.search_job_descriptions("Senior software engineer position")
    for result in job_results:
        print(f"Score: {result['score']:.3f}")
        print(f"Title: {result['metadata']['title']}")
        print(f"Company: {result['metadata']['company']}")
        print()
    
    print("\n=== Testing Question Search ===")
    question_results = rag.search_questions("API design and database optimization", category="Technical - Software Engineering")
    for result in question_results:
        print(f"Score: {result['score']:.3f}")
        print(f"Category: {result['metadata']['category']}")
        print(f"Question: {result['metadata']['question']}")
        print() 