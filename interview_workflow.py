"""
LangGraph workflow for interview planning and execution.
Handles interview plan creation and dynamic question flow with optimized prompts.
"""

import logging
from typing import Dict, List, Any, Optional, TypedDict
from dataclasses import dataclass
import json

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage

from rag_system import InterviewRAG

logger = logging.getLogger(__name__)

class InterviewState(TypedDict):
    """State for the interview workflow."""
    # Input data
    resume_content: str
    job_description: str
    candidate_name: str
    
    # Interview plan
    interview_plan: Dict[str, Any]
    current_question_index: int
    questions_list: List[Dict[str, Any]]
    
    # Interview session
    conversation_history: List[Dict[str, str]]
    current_question: str
    current_answer: str
    follow_up_needed: bool
    
    # Analysis and scoring
    answer_analysis: Dict[str, Any]
    interview_summary: Dict[str, Any]
    
    # Token tracking
    total_tokens_used: int
    
    # Status
    interview_phase: str  # planning, interviewing, completed
    error: Optional[str]

@dataclass
class InterviewPlan:
    """Structure for interview plan."""
    candidate_name: str
    position: str
    interview_duration_minutes: int
    question_categories: List[str]
    questions: List[Dict[str, Any]]
    key_skills_to_assess: List[str]
    experience_focus_areas: List[str]

class InterviewWorkflow:
    """LangGraph workflow for interview management with optimized prompts."""
    
    def __init__(self, rag_system: InterviewRAG):
        self.rag = rag_system
        # Use smaller model for token efficiency on simpler tasks
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, max_tokens=800)
        
        # Token tracking
        self.total_tokens = 0
        
        # Create the workflow graph
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow."""
        
        # Create the graph
        workflow = StateGraph(InterviewState)
        
        # Add nodes
        workflow.add_node("analyze_inputs", self._analyze_inputs)
        workflow.add_node("create_interview_plan", self._create_interview_plan)
        workflow.add_node("start_interview", self._start_interview)
        workflow.add_node("ask_question", self._ask_question)
        workflow.add_node("analyze_answer", self._analyze_answer)
        workflow.add_node("decide_follow_up", self._decide_follow_up)
        workflow.add_node("ask_follow_up", self._ask_follow_up)
        workflow.add_node("next_question", self._next_question)
        workflow.add_node("complete_interview", self._complete_interview)
        
        # Set entry point
        workflow.set_entry_point("analyze_inputs")
        
        # Add edges
        workflow.add_edge("analyze_inputs", "create_interview_plan")
        workflow.add_edge("create_interview_plan", "start_interview")
        workflow.add_edge("start_interview", "ask_question")
        workflow.add_edge("ask_question", "analyze_answer")
        workflow.add_edge("analyze_answer", "decide_follow_up")
        
        workflow.add_conditional_edges(
            "decide_follow_up",
            self._should_ask_follow_up,
            {
                "follow_up": "ask_follow_up",
                "next_question": "next_question"
            }
        )
        
        workflow.add_edge("ask_follow_up", "analyze_answer")
        
        workflow.add_conditional_edges(
            "next_question",
            self._has_more_questions,
            {
                "continue": "ask_question",
                "complete": "complete_interview"
            }
        )
        
        workflow.add_edge("complete_interview", END)
        
        return workflow.compile()
    
    def _analyze_inputs(self, state: InterviewState) -> InterviewState:
        """Analyze resume and job description to understand requirements."""
        logger.info("Analyzing inputs...")
        
        # Search for similar resumes and jobs in RAG system
        resume_matches = self.rag.search_resumes(state["resume_content"], n_results=1)
        job_matches = self.rag.search_job_descriptions(state["job_description"], n_results=1)
        
        # Optimized analysis prompt for token efficiency
        analysis_prompt = ChatPromptTemplate.from_template("""Extract key info for interview planning:

RESUME: {resume}

JOB: {job_description}

Return JSON only:
{{
  "candidate_skills": ["skill1", "skill2"],
  "job_requirements": ["req1", "req2"], 
  "skill_gaps": ["gap1", "gap2"],
  "technical_level": "junior|mid|senior",
  "behavioral_focus": ["area1", "area2"]
}}""")
        
        response = self.llm.invoke(analysis_prompt.format(
            resume=state["resume_content"][:1000],  # Limit input for token efficiency
            job_description=state["job_description"][:1000]
        ))
        
        # Track tokens
        self.total_tokens += response.response_metadata.get('token_usage', {}).get('total_tokens', 0)
        
        try:
            analysis = json.loads(response.content)
            state["interview_plan"] = {"analysis": analysis}
        except json.JSONDecodeError:
            logger.warning("Failed to parse analysis JSON, using fallback")
            state["interview_plan"] = {"analysis": {"error": "Failed to parse analysis"}}
        
        state["interview_phase"] = "planning"
        state["total_tokens_used"] = self.total_tokens
        return state
    
    def _create_interview_plan(self, state: InterviewState) -> InterviewState:
        """Create a structured interview plan based on analysis."""
        logger.info("Creating interview plan...")
        
        analysis = state["interview_plan"]["analysis"]
        
        # Determine question categories based on job requirements
        categories = ["Behavioral"]  # Always include behavioral
        
        # Add technical categories based on job type
        job_desc_lower = state["job_description"].lower()
        if any(keyword in job_desc_lower for keyword in ["software", "engineer", "developer", "programming"]):
            categories.append("Technical - Software Engineering")
        if any(keyword in job_desc_lower for keyword in ["data", "scientist", "analytics", "ml", "ai"]):
            categories.append("Technical - Data Science")
        
        categories.append("Project Deep Dive")
        
        # Get questions for each category (limited for efficiency)
        all_questions = []
        for category in categories:
            questions = self.rag.get_questions_by_category(category, n_results=2)
            for q in questions[:2]:  # Limit to 2 questions per category
                all_questions.append({
                    "category": category,
                    "question": q["metadata"]["question"],
                    "follow_up": q["metadata"].get("follow_up", ""),
                    "asked": False,
                    "answer": "",
                    "follow_up_asked": False
                })
        
        # Create interview plan
        plan = InterviewPlan(
            candidate_name=state["candidate_name"],
            position=state.get("job_description", "").split("\n")[0][:50] if state.get("job_description") else "Unknown Position",
            interview_duration_minutes=25,  # Reduced for efficiency
            question_categories=categories,
            questions=all_questions,
            key_skills_to_assess=analysis.get("job_requirements", [])[:5],  # Limit for efficiency
            experience_focus_areas=analysis.get("candidate_skills", [])[:5]
        )
        
        state["interview_plan"] = {
            "analysis": analysis,
            "plan": plan.__dict__
        }
        state["questions_list"] = all_questions
        state["current_question_index"] = 0
        state["conversation_history"] = []
        
        return state
    
    def _start_interview(self, state: InterviewState) -> InterviewState:
        """Start the interview with a greeting."""
        logger.info("Starting interview...")
        
        greeting = f"Hello {state['candidate_name']}! Thank you for your time today. I'll ask you about your background and experience. Let's begin."
        
        state["conversation_history"].append({
            "speaker": "interviewer",
            "message": greeting,
            "timestamp": "start"
        })
        
        state["interview_phase"] = "interviewing"
        return state
    
    def _ask_question(self, state: InterviewState) -> InterviewState:
        """Ask the current question."""
        logger.info(f"Asking question {state['current_question_index']}")
        
        if state["current_question_index"] < len(state["questions_list"]):
            question_data = state["questions_list"][state["current_question_index"]]
            question = question_data["question"]
            
            state["current_question"] = question
            state["questions_list"][state["current_question_index"]]["asked"] = True
            
            state["conversation_history"].append({
                "speaker": "interviewer",
                "message": question,
                "timestamp": f"question_{state['current_question_index']}"
            })
        
        return state
    
    def _analyze_answer(self, state: InterviewState) -> InterviewState:
        """Analyze the candidate's answer with optimized prompt."""
        logger.info("Analyzing answer...")
        
        if not state.get("current_answer"):
            return state
        
        # Store the answer
        state["conversation_history"].append({
            "speaker": "candidate",
            "message": state["current_answer"],
            "timestamp": f"answer_{state['current_question_index']}"
        })
        
        # Update the question with the answer
        if state["current_question_index"] < len(state["questions_list"]):
            state["questions_list"][state["current_question_index"]]["answer"] = state["current_answer"]
        
        # Optimized analysis prompt for token efficiency
        analysis_prompt = ChatPromptTemplate.from_template("""Rate this interview answer (1-5 scale):

Q: {question}
A: {answer}

Return JSON only:
{{
  "completeness": 4,
  "clarity": 5,
  "technical_depth": 3,
  "relevance": 4,
  "needs_follow_up": true,
  "follow_up_reason": "brief reason"
}}""")
        
        response = self.llm.invoke(analysis_prompt.format(
            question=state["current_question"][:200],  # Limit for token efficiency
            answer=state["current_answer"][:400]
        ))
        
        # Track tokens
        self.total_tokens += response.response_metadata.get('token_usage', {}).get('total_tokens', 0)
        state["total_tokens_used"] = self.total_tokens
        
        try:
            analysis = json.loads(response.content)
            state["answer_analysis"] = analysis
            state["follow_up_needed"] = analysis.get("needs_follow_up", False)
        except json.JSONDecodeError:
            logger.warning("Failed to parse analysis JSON")
            state["answer_analysis"] = {"error": "Failed to analyze answer"}
            state["follow_up_needed"] = False
        
        return state
    
    def _decide_follow_up(self, state: InterviewState) -> InterviewState:
        """Decide whether to ask a follow-up question."""
        # This is handled by the conditional edge
        return state
    
    def _should_ask_follow_up(self, state: InterviewState) -> str:
        """Conditional edge function to decide on follow-up."""
        if state.get("follow_up_needed", False) and state["current_question_index"] < len(state["questions_list"]):
            # Check if we haven't already asked a follow-up for this question
            current_q = state["questions_list"][state["current_question_index"]]
            if not current_q.get("follow_up_asked", False):
                return "follow_up"
        return "next_question"
    
    def _ask_follow_up(self, state: InterviewState) -> InterviewState:
        """Ask a follow-up question with optimized generation."""
        logger.info("Asking follow-up question...")
        
        current_q = state["questions_list"][state["current_question_index"]]
        
        # Use predefined follow-up or generate one
        follow_up = current_q.get("follow_up", "")
        if not follow_up:
            # Optimized follow-up generation prompt
            follow_up_prompt = ChatPromptTemplate.from_template("""Generate a brief follow-up question:

Q: {question}
A: {answer}

Follow-up (max 20 words):""")
            
            response = self.llm.invoke(follow_up_prompt.format(
                question=state["current_question"][:150],
                answer=state["current_answer"][:300]
            ))
            
            # Track tokens
            self.total_tokens += response.response_metadata.get('token_usage', {}).get('total_tokens', 0)
            state["total_tokens_used"] = self.total_tokens
            
            follow_up = response.content.strip()
        
        # Mark that we asked a follow-up
        state["questions_list"][state["current_question_index"]]["follow_up_asked"] = True
        
        state["conversation_history"].append({
            "speaker": "interviewer",
            "message": follow_up,
            "timestamp": f"follow_up_{state['current_question_index']}"
        })
        
        # Reset for next answer
        state["follow_up_needed"] = False
        
        return state
    
    def _next_question(self, state: InterviewState) -> InterviewState:
        """Move to the next question."""
        state["current_question_index"] += 1
        state["current_answer"] = ""
        return state
    
    def _has_more_questions(self, state: InterviewState) -> str:
        """Check if there are more questions to ask."""
        if state["current_question_index"] < len(state["questions_list"]):
            return "continue"
        return "complete"
    
    def _complete_interview(self, state: InterviewState) -> InterviewState:
        """Complete the interview and generate summary."""
        logger.info("Completing interview...")
        
        # Optimized summary prompt for token efficiency
        summary_prompt = ChatPromptTemplate.from_template("""Generate interview summary:

Candidate: {candidate_name}
Position: {position}

Conversation (last 3 exchanges):
{conversation}

Return JSON:
{{
  "overall_assessment": "brief assessment",
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1"],
  "technical_competency": "rating/5",
  "communication_skills": "rating/5",
  "recommendation": "hire|no_hire|more_evaluation",
  "key_highlights": ["highlight1", "highlight2"]
}}""")
        
        # Get last few conversation exchanges for efficiency
        recent_conversation = state["conversation_history"][-6:]  # Last 3 Q&A pairs
        conversation_text = "\n".join([
            f"{msg['speaker']}: {msg['message'][:100]}..."
            for msg in recent_conversation
        ])
        
        response = self.llm.invoke(summary_prompt.format(
            candidate_name=state["candidate_name"],
            position=state["interview_plan"]["plan"]["position"],
            conversation=conversation_text
        ))
        
        # Track tokens
        self.total_tokens += response.response_metadata.get('token_usage', {}).get('total_tokens', 0)
        state["total_tokens_used"] = self.total_tokens
        
        try:
            summary = json.loads(response.content)
        except json.JSONDecodeError:
            logger.warning("Failed to parse summary JSON")
            summary = {"summary": response.content[:500]}
        
        state["interview_summary"] = summary
        state["interview_phase"] = "completed"
        
        # Add closing message
        closing = f"Thank you {state['candidate_name']} for your time today. We'll be in touch soon with next steps."
        state["conversation_history"].append({
            "speaker": "interviewer",
            "message": closing,
            "timestamp": "end"
        })
        
        logger.info(f"Interview completed. Total tokens used: {self.total_tokens}")
        
        return state
    
    def run_interview_planning(self, resume_content: str, job_description: str, candidate_name: str) -> Dict[str, Any]:
        """Run the interview planning phase only."""
        initial_state = InterviewState(
            resume_content=resume_content,
            job_description=job_description,
            candidate_name=candidate_name,
            interview_plan={},
            current_question_index=0,
            questions_list=[],
            conversation_history=[],
            current_question="",
            current_answer="",
            follow_up_needed=False,
            answer_analysis={},
            interview_summary={},
            total_tokens_used=0,
            interview_phase="planning",
            error=None
        )
        
        # Run only planning steps
        state = initial_state
        state = self._analyze_inputs(state)
        state = self._create_interview_plan(state)
        state = self._start_interview(state)
        
        return state
    
    def process_answer_and_continue(self, state: InterviewState, answer: str) -> InterviewState:
        """Process an answer and continue the interview workflow."""
        state["current_answer"] = answer
        
        # Continue workflow from analyze_answer
        state = self._analyze_answer(state)
        state = self._decide_follow_up(state)
        
        # Check if we need follow-up
        if self._should_ask_follow_up(state) == "follow_up":
            state = self._ask_follow_up(state)
        else:
            state = self._next_question(state)
            
            # Check if we have more questions
            if self._has_more_questions(state) == "continue":
                state = self._ask_question(state)
            else:
                state = self._complete_interview(state)
        
        return state
    
    def get_current_question(self, state: InterviewState) -> Optional[str]:
        """Get the current question to ask."""
        if state["conversation_history"]:
            last_message = state["conversation_history"][-1]
            if last_message["speaker"] == "interviewer":
                return last_message["message"]
        return None
    
    def get_interview_metrics(self, state: InterviewState) -> Dict[str, Any]:
        """Calculate interview metrics for analytics."""
        questions_asked = sum(1 for q in state["questions_list"] if q.get("asked", False))
        questions_answered = sum(1 for q in state["questions_list"] if q.get("answer", ""))
        follow_ups_asked = sum(1 for q in state["questions_list"] if q.get("follow_up_asked", False))
        
        # Calculate average scores
        scores = []
        for q in state["questions_list"]:
            if q.get("answer"):
                # Extract scores from analysis if available
                analysis = state.get("answer_analysis", {})
                if isinstance(analysis, dict) and "completeness" in analysis:
                    scores.append({
                        "completeness": analysis.get("completeness", 0),
                        "clarity": analysis.get("clarity", 0),
                        "technical_depth": analysis.get("technical_depth", 0),
                        "relevance": analysis.get("relevance", 0)
                    })
        
        avg_scores = {}
        if scores:
            avg_scores = {
                "avg_completeness_score": sum(s["completeness"] for s in scores) / len(scores),
                "avg_clarity_score": sum(s["clarity"] for s in scores) / len(scores),
                "avg_technical_depth_score": sum(s["technical_depth"] for s in scores) / len(scores),
                "avg_relevance_score": sum(s["relevance"] for s in scores) / len(scores)
            }
        
        return {
            "total_questions": len(state["questions_list"]),
            "questions_answered": questions_answered,
            "follow_up_questions": follow_ups_asked,
            "total_tokens_used": state.get("total_tokens_used", 0),
            **avg_scores
        }

def create_interview_workflow(rag_system: InterviewRAG) -> InterviewWorkflow:
    """Factory function to create interview workflow."""
    return InterviewWorkflow(rag_system)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test the workflow
    from rag_system import initialize_rag_system
    
    rag = initialize_rag_system()
    workflow = create_interview_workflow(rag)
    
    # Test planning
    test_resume = """
    John Smith - Senior Software Engineer
    5+ years experience in Python, React, and cloud technologies.
    Built microservices architecture serving 1M+ users.
    """
    
    test_job = """
    Senior Software Engineer at TechCorp
    Requirements: 5+ years experience, Python, JavaScript, AWS
    Responsibilities: Design scalable applications, mentor developers
    """
    
    result = workflow.run_interview_planning(test_resume, test_job, "John Smith")
    print(f"Interview plan created with {len(result['questions_list'])} questions")
    print(f"First question: {workflow.get_current_question(result)}")
    print(f"Tokens used in planning: {result.get('total_tokens_used', 0)}") 