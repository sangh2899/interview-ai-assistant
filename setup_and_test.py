#!/usr/bin/env python3
"""
Setup and test script for the AI Interview Copilot Agent.
Generates mock data, tests RAG system, and workflow components.
"""

import os
import sys
import logging
import asyncio
from pathlib import Path
from dotenv import load_dotenv
# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def generate_mock_data():
    """Generate mock data for testing."""
    print("=== Generating Mock Data ===")
    from mock_data_generator import save_mock_data
    save_mock_data()
    print("✅ Mock data generated successfully!")

def test_rag_system():
    """Test the RAG system."""
    print("\n=== Testing RAG System ===")
    from rag_system import initialize_rag_system
    
    # Initialize RAG system
    rag = initialize_rag_system()
    
    # Test resume search
    print("\n--- Testing Resume Search ---")
    resume_results = rag.search_resumes("Python software engineer with API experience")
    for i, result in enumerate(resume_results):
        print(f"Result {i+1}:")
        print(f"  Score: {result['score']:.3f}")
        print(f"  Name: {result['metadata']['name']}")
        print(f"  Skills: {result['metadata']['skills']}")
        print()
    
    # Test job search
    print("--- Testing Job Search ---")
    job_results = rag.search_job_descriptions("Senior software engineer position")
    for i, result in enumerate(job_results):
        print(f"Result {i+1}:")
        print(f"  Score: {result['score']:.3f}")
        print(f"  Title: {result['metadata']['title']}")
        print(f"  Company: {result['metadata']['company']}")
        print()
    
    # Test question search
    print("--- Testing Question Search ---")
    question_results = rag.search_questions("API design and database optimization", category="Technical - Software Engineering")
    for i, result in enumerate(question_results):
        print(f"Question {i+1}:")
        print(f"  Score: {result['score']:.3f}")
        print(f"  Category: {result['metadata']['category']}")
        print(f"  Question: {result['metadata']['question']}")
        print()
    
    print("✅ RAG system test completed successfully!")

def test_interview_workflow():
    """Test the interview workflow."""
    print("\n=== Testing Interview Workflow ===")
    from rag_system import initialize_rag_system
    from interview_workflow import create_interview_workflow
    
    # Initialize systems
    rag = initialize_rag_system()
    workflow = create_interview_workflow(rag)
    
    # Test data
    test_resume = """
    John Smith - Senior Software Engineer
    5+ years experience in Python, React, and cloud technologies.
    Built microservices architecture serving 1M+ users.
    Led development of RESTful APIs using Python/FastAPI and React frontend applications.
    Skills: Python, JavaScript, React, FastAPI, PostgreSQL, AWS, Docker, Git
    """
    
    test_job = """
    Senior Software Engineer at InnovateTech Corp
    Requirements: 5+ years experience, Python, JavaScript, AWS
    Responsibilities: Design scalable applications, mentor developers
    Skills Required: Python, JavaScript, React, FastAPI, PostgreSQL, AWS, Docker, Git
    """
    
    # Test interview planning
    print("--- Testing Interview Planning ---")
    result = workflow.run_interview_planning(test_resume, test_job, "John Smith")
    
    print(f"✅ Interview plan created successfully!")
    print(f"  Candidate: {result['candidate_name']}")
    print(f"  Questions planned: {len(result['questions_list'])}")
    print(f"  Interview phase: {result['interview_phase']}")
    
    # Get first question
    first_question = workflow.get_current_question(result)
    print(f"  First question: {first_question}")
    
    # Test answer processing
    print("\n--- Testing Answer Processing ---")
    test_answer = "I have 5 years of experience in software development, primarily using Python and JavaScript. I've worked on building web applications and APIs."
    
    updated_state = workflow.process_answer_and_continue(result, test_answer)
    next_question = workflow.get_current_question(updated_state)
    
    print(f"✅ Answer processed successfully!")
    print(f"  Next question: {next_question}")
    print(f"  Current question index: {updated_state['current_question_index']}")
    
    print("✅ Interview workflow test completed successfully!")

def create_env_template():
    """Create .env.local template file."""
    print("\n=== Creating Environment Template ===")
    
    env_template = """# Environment variables for AI Interview Copilot Agent
# Copy this to .env.local and fill in your API keys

# Required for LiveKit
LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=

# Required for OpenAI (LLM and embeddings)
OPENAI_API_KEY=

# Required for Cartesia (TTS)
CARTESIA_API_KEY=

# Required for Deepgram (STT)
DEEPGRAM_API_KEY=

# Optional for Tavily search
TAVILY_API_KEY=
"""
    
    if not os.path.exists(".env.example"):
        with open(".env.example", "w") as f:
            f.write(env_template)
        print("✅ Created .env.example template")
    else:
        print("ℹ️ .env.example already exists")
    
    if not os.path.exists(".env.local"):
        print("⚠️ Please copy .env.example to .env.local and fill in your API keys")
    else:
        print("✅ .env.local exists")

def check_dependencies():
    """Check if all required dependencies are available."""
    print("\n=== Checking Dependencies ===")
    
    required_packages = [
        "livekit-agents",
        "livekit-plugins-openai", 
        "livekit-plugins-cartesia",
        "livekit-plugins-deepgram",
        "livekit-plugins-silero",
        "langgraph",
        "langchain",
        "langchain-openai",
        "chromadb",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies are installed!")
        return True

def main():
    """Main setup and test function."""
    setup_logging()
    
    print("🤖 AI Interview Copilot Agent - Setup & Test")
    print("=" * 50)
    
    # Check dependencies
    # if not check_dependencies():
    #     print("\n❌ Please install missing dependencies first")
    #     return 1
    
    # Create environment template
    create_env_template()
    
    # Check if API keys are configured
    if not os.path.exists(".env.local"):
        print("\n⚠️ Environment not configured. Please:")
        print("1. Copy .env.example to .env.local")
        print("2. Fill in your API keys")
        print("3. Run this script again")
        return 1

    load_dotenv(dotenv_path=".env.local")
    try:
        # Generate mock data
        generate_mock_data()
        
        # Test RAG system
        test_rag_system()
        
        # Test interview workflow
        test_interview_workflow()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed! The system is ready to use.")
        print("\nTo run the interview agent:")
        print("  python interview_agent.py dev")
        print("\nTo run individual components:")
        print("  python rag_system.py          # Test RAG system")
        print("  python interview_workflow.py  # Test workflow")
        print("  python mock_data_generator.py # Generate fresh mock data")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during setup/testing: {e}")
        logging.exception("Setup/test error")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 