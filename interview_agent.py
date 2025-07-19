"""
Voice Interview Agent using LiveKit, LangGraph, and RAG.
Conducts voice-based interviews with real-time transcription and PostgreSQL persistence.
"""

import logging
import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import wave

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    metrics,
    RoomInputOptions,
)
from livekit.plugins import (
    cartesia,
    openai,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from rag_system import initialize_rag_system
from interview_workflow import create_interview_workflow, InterviewState

load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("interview-agent")

class InterviewAgent(Agent):
    """Voice interview agent with LangGraph workflow integration and PostgreSQL persistence."""
    
    def __init__(self):
        """Initialize the interview agent."""
        super().__init__(
            instructions=(
                "You are a professional AI interviewer. Ask structured questions based on "
                "the candidate's resume and job requirements. Listen carefully and ask "
                "relevant follow-ups. Be professional, encouraging, and thorough. "
                "Keep responses concise for voice interaction."
            ),
            stt=deepgram.STT(),
            llm=openai.LLM(model="gpt-4o-mini"),
            tts=cartesia.TTS(),
            turn_detection=MultilingualModel(),
        )
        
        # Initialize RAG and workflow systems
        self.rag_system = None
        self.interview_workflow = None
        self.interview_state = None
        
        # Interview session data
        self.candidate_name = ""
        self.interview_start_time = None
        self.interview_id = None
        self.session_id = None  # Database session ID
        
        # Token tracking
        self.total_tokens_used = 0
    
    async def initialize_systems(self):
        """Initialize RAG and workflow systems."""
        logger.info("Initializing RAG and workflow systems...")
        try:
            self.rag_system = initialize_rag_system()
            self.interview_workflow = create_interview_workflow(
                self.rag_system
            )
            logger.info("Systems initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize systems: {e}")
            raise
    
    async def start_interview(self, resume_content: str, job_description: str, candidate_name: str):
        """Start a new interview session."""
        logger.info(f"Starting interview for {candidate_name}")
        
        self.candidate_name = candidate_name
        self.interview_start_time = datetime.now()
        self.interview_id = f"interview_{candidate_name.replace(' ', '_')}_{int(self.interview_start_time.timestamp())}"
        
        # Create interview plan using workflow
        self.interview_state = self.interview_workflow.run_interview_planning(
            resume_content, job_description, candidate_name
        )
        
        # Track tokens from planning
        self.total_tokens_used = self.interview_state.get("total_tokens_used", 0)
        
        # Save initial interview session to database
        await self.save_interview_session_to_db(status="in_progress")
        
        # Get the initial greeting/question
        current_question = self.interview_workflow.get_current_question(self.interview_state)
        if current_question:
            return current_question
        
        return "Hello! I'm ready to begin your interview. Please introduce yourself."
    
    async def process_candidate_response(self, response: str) -> str:
        """Process candidate's response and get next question."""
        logger.info("Processing candidate response...")
        
        if not self.interview_state:
            return "I'm sorry, but the interview hasn't been properly initialized. Please try again."
        
        # Process the answer through the workflow
        self.interview_state = self.interview_workflow.process_answer_and_continue(
            self.interview_state, response
        )
        
        # Update token tracking
        self.total_tokens_used = self.interview_state.get("total_tokens_used", 0)
        
        # Get the next question or completion message
        next_question = self.interview_workflow.get_current_question(self.interview_state)
        
        if next_question:
            return next_question
        
        # Interview completed
        if self.interview_state.get("interview_phase") == "completed":
            await self.save_interview_results()
            return "Thank you for your time today. The interview has been completed successfully. We'll be in touch with next steps soon!"
        
        return "Let me think of the next question..."
    
    async def save_interview_session_to_db(self, status: str = "in_progress"):
        """Save interview session to PostgreSQL database."""
        if not self.rag_system or not self.interview_state:
            return
        
        interview_data = {
            "interview_id": self.interview_id,
            "candidate_name": self.candidate_name,
            "start_time": self.interview_start_time,
            "end_time": datetime.now() if status == "completed" else None,
            "status": status,
            "resume_content": self.interview_state.get("resume_content"),
            "job_description": self.interview_state.get("job_description"),
            "interview_plan": self.interview_state.get("interview_plan"),
            "questions_and_answers": self.interview_state.get("questions_list"),
            "interview_summary": self.interview_state.get("interview_summary"),
            "transcription": self.interview_state.get("conversation_history")
        }
        
        self.session_id = self.rag_system.save_interview_session(interview_data)
        if self.session_id:
            logger.info(f"Interview session saved to database with ID: {self.session_id}")
    
    async def save_interview_results(self):
        """Save final interview results to database."""
        logger.info("Saving interview results...")
        
        try:
            # Update interview session with completion status
            await self.save_interview_session_to_db(status="completed")
            
            # Calculate and save interview metrics
            if self.interview_workflow and self.interview_state:
                metrics_data = self.interview_workflow.get_interview_metrics(self.interview_state)
                
                # Add duration calculation
                if self.interview_start_time:
                    duration = (datetime.now() - self.interview_start_time).total_seconds() / 60
                    metrics_data["total_duration_minutes"] = duration
                
                # Add token usage
                metrics_data["total_tokens_used"] = self.total_tokens_used
                
                # Save metrics to database
                metrics_id = self.rag_system.save_interview_metrics(self.interview_id, metrics_data)
                if metrics_id:
                    logger.info(f"Interview metrics saved with ID: {metrics_id}")
            
            logger.info(f"Interview results saved successfully. Total tokens used: {self.total_tokens_used}")
            
        except Exception as e:
            logger.error(f"Failed to save interview results: {e}")
    
    async def on_enter(self):
        """Called when agent enters the room."""
        logger.info("Interview agent entered the room")
        
        # Initialize systems if not already done
        if not self.rag_system:
            await self.initialize_systems()
        
        # For demo purposes, use predefined resume and job description
        # In a real application, these would be provided by the user
        demo_resume = """
        John Smith
        Senior Software Engineer
        Email: john.smith@email.com
        Phone: +1-555-0123
        
        Summary: Senior Software Engineer with 5+ years of experience in full-stack development using Python, React, and cloud technologies.
        
        Experience:
        - Senior Software Engineer at TechCorp Inc. (2021-2024)
          Led development of microservices architecture serving 1M+ users. Built RESTful APIs using Python/FastAPI and React frontend applications.
        
        - Software Engineer at StartupXYZ (2019-2021)
          Developed web applications using Django and PostgreSQL. Implemented CI/CD pipelines and automated testing frameworks.
        
        Education:
        - Bachelor of Science in Computer Science, State University (2019)
        
        Skills: Python, JavaScript, React, FastAPI, PostgreSQL, AWS, Docker, Git
        
        Projects:
        - E-commerce Platform: Built a full-stack e-commerce platform using React and Python FastAPI with payment integration
        - Task Management API: Developed RESTful API for task management with user authentication and real-time updates
        """
        
        demo_job_description = """
        Senior Software Engineer
        InnovateTech Corp
        
        We are seeking a Senior Software Engineer to join our engineering team. The ideal candidate will have 5+ years of experience in software development and be proficient in modern web technologies.
        
        Requirements:
        - Bachelor's degree in Computer Science or related field
        - 5+ years of software development experience
        - Strong proficiency in Python and JavaScript
        - Experience with cloud platforms (AWS, Azure, or GCP)
        - Knowledge of microservices architecture
        
        Responsibilities:
        - Design and develop scalable web applications
        - Lead technical discussions and code reviews
        - Mentor junior developers
        - Collaborate with product managers and designers
        - Implement best practices for code quality and testing
        
        Skills Required: Python, JavaScript, React, FastAPI, PostgreSQL, AWS, Docker, Git
        Experience: 5-8 years
        """
        
        # Start the interview
        initial_message = await self.start_interview(demo_resume, demo_job_description, "John Smith")
        
        # Send the initial message
        await self.say(initial_message, allow_interruptions=True)
    
    async def on_user_speech(self, user_speech):
        """Handle user speech input from LiveKit."""
        logger.info(f"Received candidate speech: {user_speech.alternatives[0].text[:100] if user_speech.alternatives else 'No text'}...")
        
        try:
            # Get the transcribed text
            response_text = user_speech.alternatives[0].text if user_speech.alternatives else ""
            
            if response_text.strip():
                # Process the response and get next question
                next_message = await self.process_candidate_response(response_text)
                
                # Send the next question or completion message
                await self.say(next_message, allow_interruptions=True)
            
        except Exception as e:
            logger.error(f"Error processing candidate response: {e}")
            await self.say("I'm sorry, I encountered an issue. Could you please repeat your answer?", allow_interruptions=True)

def prewarm(proc: JobProcess):
    """Prewarm function to initialize VAD model."""
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    """Main entrypoint for the interview agent."""
    logger.info(f"Connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    
    # Wait for the first participant to connect
    participant = await ctx.wait_for_participant()
    logger.info(f"Starting interview agent for participant {participant.identity}")
    
    usage_collector = metrics.UsageCollector()
    
    # Log metrics and collect usage data
    def on_metrics_collected(agent_metrics: metrics.AgentMetrics):
        metrics.log_metrics(agent_metrics)
        usage_collector.collect(agent_metrics)
    
    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        # Optimized for interview context - shorter delays for better flow
        min_endpointing_delay=0.8,  # Slightly shorter for better responsiveness
        max_endpointing_delay=8.0,  # Reduced from 10.0 for efficiency
    )
    
    # Trigger the on_metrics_collected function when metrics are collected
    session.on("metrics_collected", on_metrics_collected)
    
    await session.start(
        room=ctx.room,
        agent=InterviewAgent(),
        room_input_options=RoomInputOptions(
            # Enable background voice & noise cancellation for better audio quality
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the agent
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    ) 