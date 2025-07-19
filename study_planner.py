from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import json
import logging
import re
import time
from questions import (
    get_questions_by_category,
    get_best_practices,
)
from config import get_openai_config

logger = logging.getLogger(__name__)


class StudyPlanState(TypedDict):
    """State for the study plan workflow."""

    resume_content: str
    improvement_areas: List[str]
    technical_skills: List[str]
    experience_level: str
    study_plan: Dict[str, Any]
    interview_practices: List[str]
    behavioral_questions: List[Dict[str, str]]  # question and detailed_answer
    technical_questions: Dict[str, List[Dict[str, str]]]  # question and detailed_answer
    final_output: Dict[str, Any]


class InterviewStudyPlanner:
    """LangGraph workflow for creating personalized interview study plans."""

    def __init__(self, model_name: str = "gpt-4o", fast_mode: bool = False):
        """
        Initialize the study planner.

        Args:
            model_name: The OpenAI model to use (default: gpt-4o)
            fast_mode: If True, use keyword-based analysis instead of API calls (default: False)
        """
        self.fast_mode = fast_mode

        if not fast_mode:
            # Get OpenAI configuration for API mode
            config = get_openai_config()

            # Override model name if provided
            if model_name != "gpt-4o":
                config.model_name = model_name

            # Initialize ChatOpenAI with configuration
            self.llm = ChatOpenAI(**config.get_chatgpt_config())
            self.graph = self._build_graph()
        else:
            # Initialize fast mode patterns
            self._init_fast_mode_patterns()

    def _init_fast_mode_patterns(self):
        """Initialize patterns for fast keyword-based analysis."""
        self.technical_skills_patterns = {
            "python": r"\b(python|django|flask|fastapi|pandas|numpy)\b",
            "javascript": r"\b(javascript|js|react|vue|angular|node\.?js|express)\b",
            "java": r"\b(java|spring|hibernate|maven|gradle)\b(?!script)",
            "cpp": r"\b(c\+\+|cpp|c plus plus)\b",
            "c": r"\bc\b(?!\+)",
            "sql": r"\b(sql|mysql|postgresql|oracle|mongodb)\b",
            "aws": r"\b(aws|amazon web services|ec2|s3|lambda)\b",
            "docker": r"\b(docker|kubernetes|k8s|container)\b",
            "git": r"\b(git|github|gitlab|version control)\b",
        }

        self.improvement_patterns = {
            "leadership": r"\b(lead|manage|leadership|team lead|mentor|supervise)\b",
            "system_design": r"\b(system design|architecture|scalability|microservices)\b",
            "communication": r"\b(communication|presentation|stakeholder|client)\b",
            "technical_skills": r"\b(technical|programming|coding|development)\b",
            "project_management": r"\b(project management|agile|scrum|planning)\b",
        }

        self.experience_patterns = {
            "senior": r"\b(senior|lead|principal|architect|expert|5\+?\s*years?|[6-9]\+?\s*years?|\d{2}\+?\s*years?)\b",
            "mid": r"\b(mid|middle|3\+?\s*years?|4\+?\s*years?|5\s*years?)\b",
            "entry": r"\b(entry|junior|new|graduate|fresh|1\+?\s*years?|2\+?\s*years?)\b",
        }

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(StudyPlanState)

        # Add nodes
        workflow.add_node("analyze_resume", self._analyze_resume)
        workflow.add_node("generate_best_practices", self._generate_best_practices)
        workflow.add_node(
            "generate_behavioral_questions", self._generate_behavioral_questions
        )
        workflow.add_node(
            "generate_technical_questions", self._generate_technical_questions
        )
        workflow.add_node("create_study_plan", self._create_study_plan)

        # Add edges
        workflow.set_entry_point("analyze_resume")
        workflow.add_edge("analyze_resume", "generate_best_practices")
        workflow.add_edge("generate_best_practices", "generate_behavioral_questions")
        workflow.add_edge(
            "generate_behavioral_questions", "generate_technical_questions"
        )
        workflow.add_edge("generate_technical_questions", "create_study_plan")
        workflow.add_edge("create_study_plan", END)

        return workflow.compile()

    def _analyze_resume_fast(self, resume_content: str) -> Dict[str, Any]:
        """Fast resume analysis using keyword matching."""
        logger.info("Analyzing resume using fast mode...")
        resume_lower = resume_content.lower()

        # Extract technical skills
        technical_skills = []
        for skill, pattern in self.technical_skills_patterns.items():
            if re.search(pattern, resume_lower, re.IGNORECASE):
                technical_skills.append(skill)

        # Extract improvement areas
        improvement_areas = []
        for area, pattern in self.improvement_patterns.items():
            if re.search(pattern, resume_lower, re.IGNORECASE):
                improvement_areas.append(area)

        # Determine experience level
        experience_level = "mid"  # default
        for level, pattern in self.experience_patterns.items():
            if re.search(pattern, resume_lower, re.IGNORECASE):
                experience_level = level
                break

        # Default values if nothing found
        if not technical_skills:
            technical_skills = ["python", "javascript"]
        if not improvement_areas:
            improvement_areas = ["technical_skills", "communication"]

        return {
            "technical_skills": technical_skills,
            "improvement_areas": improvement_areas,
            "experience_level": experience_level,
        }

    def _get_best_practices_fast(
        self, experience_level: str, improvement_areas: List[str]
    ) -> List[str]:
        """Get best practices based on experience level and improvement areas."""
        base_practices = [
            "Practice the STAR method for behavioral questions",
            "Prepare specific examples from your experience",
            "Research the company and role thoroughly",
            "Prepare thoughtful questions to ask the interviewer",
            "Practice explaining your technical projects clearly",
        ]

        if experience_level == "entry":
            base_practices.extend(
                [
                    "Focus on learning ability and enthusiasm",
                    "Prepare examples from internships, projects, or coursework",
                    "Show willingness to learn and grow",
                ]
            )
        elif experience_level == "senior":
            base_practices.extend(
                [
                    "Prepare leadership and mentoring examples",
                    "Focus on system design and architecture decisions",
                    "Demonstrate business impact of your work",
                ]
            )

        if "leadership" in improvement_areas:
            base_practices.append("Prepare examples of leading teams or projects")

        if "communication" in improvement_areas:
            base_practices.append(
                "Practice explaining technical concepts to non-technical audiences"
            )

        return base_practices[:8]  # Limit to 8 practices

    def _get_behavioral_questions_fast(
        self, improvement_areas: List[str]
    ) -> List[Dict[str, str]]:
        """Get behavioral questions with detailed answers."""
        questions = [
            {
                "question": "Tell me about a challenging project you worked on",
                "detailed_answer": """Use the STAR method to structure your answer:

**Situation:** Set the context - describe the project, team size, timeline, and why it was challenging
**Task:** Explain your specific role and responsibilities in the project
**Action:** Detail the specific steps you took to address the challenges, including:
- Problem-solving approaches you used
- How you collaborated with team members
- Any innovative solutions you implemented
**Result:** Share the outcomes, including:
- Quantifiable results (performance improvements, cost savings, etc.)
- What you learned from the experience
- How it contributed to your professional growth

**Example structure:**
"In my previous role at [Company], our team was tasked with [specific project]. The main challenge was [specific challenge]. As the [your role], I was responsible for [your responsibilities]. I approached this by [your actions]. As a result, we achieved [specific outcomes] and I learned [key learnings]."
""",
            },
            {
                "question": "Describe a time you had to learn something new quickly",
                "detailed_answer": """Focus on demonstrating your learning agility and adaptability:

**Key elements to include:**
- **Context:** What new technology/skill you needed to learn and why
- **Timeline:** How quickly you needed to learn it
- **Learning strategy:** Your approach to learning (resources, practice, mentorship)
- **Application:** How you applied the new knowledge in practice
- **Results:** The successful outcome of using your new knowledge

**Learning strategies to mention:**
- Official documentation and tutorials
- Online courses or training materials
- Seeking guidance from experienced colleagues
- Hands-on practice and experimentation
- Building small projects to reinforce learning

**Show continuous learning:** Demonstrate that learning new things is a regular part of your professional development, not just something you do when forced to.
""",
            },
        ]

        if "leadership" in improvement_areas:
            questions.append(
                {
                    "question": "Tell me about a time you had to lead a team through a difficult situation",
                    "detailed_answer": """Demonstrate your leadership skills and emotional intelligence:

**Leadership aspects to highlight:**
- **Vision:** How you communicated the goal and motivated the team
- **Decision-making:** How you made tough decisions under pressure
- **Support:** How you supported team members through challenges
- **Communication:** How you kept stakeholders informed
- **Results:** The positive outcome achieved through your leadership

**Key leadership qualities to demonstrate:**
- Empathy and understanding of team members' concerns
- Clear communication and transparency
- Ability to make decisions with incomplete information
- Resilience and maintaining team morale
- Learning from the experience to become a better leader
""",
                }
            )

        if "communication" in improvement_areas:
            questions.append(
                {
                    "question": "Describe a time you had to explain a complex technical concept to a non-technical audience",
                    "detailed_answer": """Show your ability to communicate effectively across different audiences:

**Communication strategies to mention:**
- **Know your audience:** Understanding their background and needs
- **Simplify without condescending:** Use analogies and everyday examples
- **Visual aids:** Diagrams, charts, or demonstrations when appropriate
- **Check understanding:** Asking questions to ensure comprehension
- **Be patient:** Allowing time for questions and clarification

**Structure your example:**
- What was the technical concept and why did you need to explain it?
- Who was your audience and what was their technical background?
- What approach did you take to make it understandable?
- How did you verify they understood?
- What was the positive outcome?

**Demonstrate empathy:** Show that you understand it can be challenging for non-technical people to grasp technical concepts, and that you approach these conversations with patience and respect.
""",
                }
            )

        return questions

    def _get_technical_questions_fast(
        self, technical_skills: List[str], experience_level: str
    ) -> Dict[str, List[Dict[str, str]]]:
        """Get technical questions based on skills."""
        technical_questions = {}

        # Programming language questions
        if "python" in technical_skills:
            technical_questions["Python Programming"] = [
                {
                    "question": "What are Python decorators and when would you use them?",
                    "detailed_answer": """**Definition:** Decorators are functions that modify or extend the behavior of other functions or classes without permanently modifying their code.

**Syntax:**
```python
@decorator_function
def my_function():
    pass
```

**Common use cases:**
1. **Logging:** Track function calls and execution time
2. **Authentication:** Check user permissions before function execution
3. **Caching:** Store results of expensive function calls
4. **Validation:** Validate function inputs
5. **Rate limiting:** Control how often a function can be called

**Example:**
```python
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@timer_decorator
def slow_function():
    time.sleep(1)
    return "Done"
```

**Built-in decorators:**
- `@property`: Create getter/setter methods
- `@staticmethod`: Methods that don't access instance or class data
- `@classmethod`: Methods that receive class as first argument
""",
                },
                {
                    "question": "Explain the difference between lists and tuples in Python",
                    "detailed_answer": """**Key Differences:**

**1. Mutability:**
- **Lists:** Mutable (can be modified after creation)
- **Tuples:** Immutable (cannot be modified after creation)

```python
# Lists
my_list = [1, 2, 3]
my_list.append(4)  # Works
my_list[0] = 10    # Works

# Tuples
my_tuple = (1, 2, 3)
my_tuple.append(4)  # Error!
my_tuple[0] = 10    # Error!
```

**2. Performance:**
- **Tuples:** Faster for iteration and access (optimized in memory)
- **Lists:** Slightly slower due to mutability overhead

**3. Use Cases:**
- **Lists:** When you need to modify the collection (add, remove, change items)
- **Tuples:** For fixed collections, coordinates, database records, dictionary keys

**4. Memory:**
- **Tuples:** Use less memory
- **Lists:** Use more memory due to over-allocation for growth

**When to use each:**
- Use **tuples** for fixed data that won't change (coordinates, RGB values, database records)
- Use **lists** for collections that will be modified (shopping cart, user input processing)
""",
                },
            ]

        if "javascript" in technical_skills:
            technical_questions["JavaScript Programming"] = [
                {
                    "question": "Explain closures in JavaScript",
                    "detailed_answer": """**Definition:** A closure is created when a function is defined inside another function and has access to variables from the outer function's scope, even after the outer function has finished executing.

**Key Concepts:**
1. **Lexical Scoping:** Functions have access to variables in their outer scope
2. **Persistence:** Variables in the outer scope remain accessible
3. **Data Privacy:** Can create private variables

**Example:**
```javascript
function outerFunction(x) {
    // This variable is in the outer scope
    let outerVariable = x;
    
    function innerFunction(y) {
        // This inner function has access to outerVariable
        console.log(outerVariable + y);
    }
    
    return innerFunction;
}

const myClosure = outerFunction(10);
myClosure(5); // Outputs: 15
```

**Practical Uses:**
1. **Module Pattern:** Creating private methods and variables
2. **Event Handlers:** Maintaining state in callbacks
3. **Function Factories:** Creating specialized functions
4. **Data Privacy:** Encapsulating data

**Common Interview Example:**
```javascript
// Problem: What will this print?
for (var i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100);
}
// Prints: 3, 3, 3 (not 0, 1, 2)

// Solution using closure:
for (let i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100);
}
// Prints: 0, 1, 2
```
""",
                }
            ]

        # Add algorithm questions for mid+ level
        if experience_level in ["mid", "senior"]:
            technical_questions["Algorithms & Data Structures"] = [
                {
                    "question": "Implement a function to find two numbers in an array that sum to a target value",
                    "detailed_answer": """**Problem:** Two Sum - Given an array of integers and a target sum, return indices of two numbers that add up to the target.

**Approach 1: Brute Force**
```python
def two_sum_brute_force(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

# Time: O(n²), Space: O(1)
```

**Approach 2: Hash Map (Optimal)**
```python
def two_sum(nums, target):
    num_map = {}  # value -> index
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    
    return []

# Time: O(n), Space: O(n)
```

**Key Insights:**
1. **Trade-off:** Space for time complexity improvement
2. **Hash Map:** Provides O(1) lookup time
3. **One Pass:** We can build the hash map while searching

**Edge Cases to Consider:**
- Empty array
- No solution exists
- Duplicate numbers
- Negative numbers

**Follow-up Questions:**
- What if the array is sorted? (Two-pointer technique)
- What if we need all pairs that sum to target?
- What about three numbers that sum to target?
""",
                }
            ]

        return technical_questions

    def _analyze_resume(self, state: StudyPlanState) -> StudyPlanState:
        """Analyze the resume to extract improvement areas and technical skills."""
        logger.info("Analyzing resume...")

        system_prompt = """
        You are an expert career coach analyzing a resume. Extract the following information:
        1. Areas that need improvement (mentioned explicitly or implied)
        2. Technical skills and programming languages mentioned
        3. Experience level (entry, mid, senior, expert)
        
        Return your analysis in the following JSON format:
        {
            "improvement_areas": ["area1", "area2", ...],
            "technical_skills": ["skill1", "skill2", ...],
            "experience_level": "entry|mid|senior|expert"
        }
        """

        human_prompt = f"Analyze this resume:\n\n{state['resume_content']}"

        try:
            response = self.llm.invoke(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=human_prompt),
                ]
            )

            analysis = json.loads(response.content)

            state["improvement_areas"] = analysis.get("improvement_areas", [])
            state["technical_skills"] = analysis.get("technical_skills", [])
            state["experience_level"] = analysis.get("experience_level", "mid")

            logger.info(
                f"Identified {len(state['improvement_areas'])} improvement areas"
            )

        except Exception as e:
            logger.error(f"Error analyzing resume: {str(e)}")
            # Fallback to default values
            state["improvement_areas"] = ["technical skills", "leadership"]
            state["technical_skills"] = ["python", "javascript"]
            state["experience_level"] = "mid"

        return state

    def _generate_best_practices(self, state: StudyPlanState) -> StudyPlanState:
        """Generate interview best practices based on experience level."""
        logger.info("Generating best practices...")

        # Get general best practices
        general_practices = get_best_practices("general")
        technical_practices = get_best_practices("technical")
        behavioral_practices = get_best_practices("behavioral")

        # Customize based on experience level
        system_prompt = f"""
        You are an interview coach. Based on the candidate's experience level ({state['experience_level']}) 
        and improvement areas ({', '.join(state['improvement_areas'])}), 
        select and customize the most relevant interview best practices.
        
        Focus on practices that will help address their specific improvement areas.
        Return a list of 8-10 practical, actionable tips.
        """

        all_practices = general_practices + technical_practices + behavioral_practices
        human_prompt = f"From these practices: {json.dumps(all_practices)}, select and customize the most relevant ones."

        try:
            response = self.llm.invoke(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=human_prompt),
                ]
            )

            # Parse the response to extract practices
            practices_text = response.content
            practices = [
                line.strip()
                for line in practices_text.split("\n")
                if line.strip() and not line.strip().startswith("#")
            ]

            state["interview_practices"] = practices[:10]  # Limit to 10 practices

        except Exception as e:
            logger.error(f"Error generating best practices: {str(e)}")
            state["interview_practices"] = general_practices[:8]

        return state

    def _generate_behavioral_questions(self, state: StudyPlanState) -> StudyPlanState:
        """Generate behavioral questions with detailed answers."""
        logger.info("Generating behavioral questions with detailed answers...")

        behavioral_questions = get_questions_by_category("behavioral", count=10)
        leadership_questions = get_questions_by_category("leadership", count=8)
        soft_skill_questions = get_questions_by_category("soft_skills", count=8)

        system_prompt = f"""
        You are an expert interview coach. Based on the candidate's improvement areas: {', '.join(state['improvement_areas'])},
        select the most relevant behavioral questions and provide comprehensive, detailed answers.
        
        For each question, provide a detailed answer that:
        1. Uses the STAR method (Situation, Task, Action, Result)
        2. Includes specific examples and scenarios
        3. Shows how to address the improvement areas
        4. Provides concrete tips and strategies
        
        Return exactly 8 questions in the following JSON format:
        [
            {{
                "question": "Tell me about a time when you had to lead a difficult project?",
                "detailed_answer": "Here's how to structure your answer using the STAR method:\n\nSituation: Set up the context. For example: 'In my previous role as a Senior Developer at TechCorp, our team was tasked with migrating a legacy system that was critical to daily operations. The timeline was tight - 3 months - and we had to do it without any downtime.'\n\nTask: Explain your responsibility. 'As the technical lead, I was responsible for planning the migration strategy, coordinating with 5 team members, and ensuring zero service interruption for our 10,000+ daily users.'\n\nAction: Detail what you did. 'I started by conducting a thorough analysis of the legacy system, breaking down the migration into smaller, manageable phases. I implemented a blue-green deployment strategy, set up comprehensive monitoring, and created detailed rollback procedures. I also organized daily standups and weekly stakeholder updates to maintain transparency.'\n\nResult: Share the outcome. 'We successfully completed the migration 2 weeks ahead of schedule with zero downtime. The new system improved performance by 40% and reduced maintenance costs by 30%. The project became a template for future migrations in the company.'\n\nKey tips: Always quantify your results, show leadership skills, and demonstrate problem-solving abilities."
            }}
        ]
        """

        all_questions = (
            behavioral_questions + leadership_questions + soft_skill_questions
        )
        human_prompt = f"From these questions: {json.dumps(all_questions)}, select the 8 most relevant ones for someone with improvement areas in {', '.join(state['improvement_areas'])} and provide detailed, comprehensive answers."

        try:
            response = self.llm.invoke(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=human_prompt),
                ]
            )

            try:
                questions_with_answers = json.loads(response.content)
                if (
                    isinstance(questions_with_answers, list)
                    and len(questions_with_answers) > 0
                ):
                    state["behavioral_questions"] = questions_with_answers[:8]
                else:
                    raise ValueError("Invalid response format")
            except (json.JSONDecodeError, ValueError):
                # Fallback: create detailed question-answer pairs
                fallback_questions = []
                for q in behavioral_questions[:8]:
                    fallback_questions.append(
                        {
                            "question": q,
                            "detailed_answer": f"""Here's how to answer this question effectively:

STAR Method Structure:
- Situation: Describe the context and background of your example
- Task: Explain your specific responsibility or challenge
- Action: Detail the steps you took to address the situation
- Result: Share the outcome and what you learned

Example Answer Framework:
"In my role at [Company], I encountered a situation where [describe context]. My responsibility was to [explain task]. I approached this by [describe your actions step by step]. As a result, [share specific outcomes with numbers if possible]. This experience taught me [key learning]."

Key Tips:
- Use specific, concrete examples from your experience
- Quantify results whenever possible (percentages, dollar amounts, time saved)
- Focus on your individual contributions while acknowledging team efforts
- Show how you've grown from the experience
- Connect your answer to the role you're applying for""",
                        }
                    )
                state["behavioral_questions"] = fallback_questions

        except Exception as e:
            logger.error(f"Error generating behavioral questions: {str(e)}")
            # Fallback to detailed format
            fallback_questions = []
            for q in behavioral_questions[:8]:
                fallback_questions.append(
                    {
                        "question": q,
                        "detailed_answer": """Use the STAR method to structure your answer:

Situation: Set the context with specific details about when and where this happened.
Task: Clearly explain what you needed to accomplish or what challenge you faced.
Action: Describe the specific steps you took, focusing on your individual contributions.
Result: Share the outcome, including quantifiable results when possible.

Remember to:
- Choose examples that highlight relevant skills for the role
- Be specific and avoid generalizations
- Show growth and learning from the experience
- Practice your examples beforehand to sound natural""",
                    }
                )
            state["behavioral_questions"] = fallback_questions

        return state

    def _generate_technical_questions(self, state: StudyPlanState) -> StudyPlanState:
        """Generate technical questions based on skills and improvement areas with answers."""
        logger.info("Generating technical questions with answers...")

        technical_questions = {}

        # Programming language questions
        for skill in state["technical_skills"]:
            skill_lower = skill.lower()
            if skill_lower in ["python", "javascript", "java", "cpp", "c++"]:
                lang_key = "cpp" if skill_lower in ["cpp", "c++"] else skill_lower
                questions = get_questions_by_category(
                    "programming_languages", lang_key, count=5
                )
                if questions:
                    # Generate answers for programming questions
                    questions_with_answers = self._generate_programming_answers(
                        questions, skill
                    )
                    technical_questions[f"{skill} Programming"] = questions_with_answers

        # LeetCode questions with solutions
        leetcode_questions = get_questions_by_category("leetcode", count=6)
        leetcode_with_answers = self._generate_leetcode_answers(leetcode_questions)
        technical_questions["LeetCode Problems"] = leetcode_with_answers

        # Code review questions
        code_review_questions = get_questions_by_category("code_review", count=4)
        code_review_with_answers = self._generate_code_review_answers(
            code_review_questions
        )
        technical_questions["Code Review & Improvement"] = code_review_with_answers

        # System design (for mid+ level)
        if state["experience_level"] in ["mid", "senior", "expert"]:
            system_design_questions = get_questions_by_category(
                "system_design", count=3
            )
            system_design_with_answers = self._generate_system_design_answers(
                system_design_questions
            )
            technical_questions["System Design"] = system_design_with_answers

        state["technical_questions"] = technical_questions
        return state

    def _generate_programming_answers(
        self, questions: List[str], language: str
    ) -> List[Dict[str, str]]:
        """Generate detailed answers for programming language questions with code examples."""
        system_prompt = f"""
        You are a senior {language} developer providing comprehensive, detailed answers to technical questions.
        For each question, provide:
        1. A thorough explanation of the concept
        2. Practical code examples that demonstrate the concept
        3. Best practices and common pitfalls
        4. Real-world use cases

        Return in JSON format:
        [
            {{
                "question": "original question",
                "detailed_answer": "Comprehensive explanation with code examples, best practices, and practical insights. Include working code snippets with comments explaining each part."
            }}
        ]
        
        Make sure the detailed_answer is comprehensive and includes:
        - Clear conceptual explanation
        - Multiple code examples with comments
        - Comparison with alternatives when relevant
        - Best practices and common mistakes to avoid
        - Performance considerations when applicable
        """

        try:
            response = self.llm.invoke(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(
                        content=f"Provide detailed answers with code examples for these {language} questions: {json.dumps(questions)}"
                    ),
                ]
            )

            try:
                return json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback format with detailed answers
                return [
                    {
                        "question": q,
                        "detailed_answer": f"""This is a fundamental {language} concept that's important to understand thoroughly.

**Explanation:**
{q.replace('?', '')} is a core concept in {language} programming that involves understanding the underlying mechanisms and best practices.

**Code Example:**
```{language.lower()}
# Example demonstrating the concept
# Add your specific implementation here
def example_function():
    '''
    This function demonstrates the concept
    '''
    pass
```

**Best Practices:**
- Study the official {language} documentation
- Practice with hands-on examples
- Understand the underlying implementation
- Consider performance implications
- Learn from real-world use cases

**Common Mistakes to Avoid:**
- Don't just memorize the syntax, understand the concepts
- Practice with different scenarios
- Consider edge cases in your implementations

**When to Use:**
This concept is particularly useful when working on projects that require [specific use case]. Understanding this will help you write more efficient and maintainable code.""",
                    }
                    for q in questions
                ]
        except Exception as e:
            logger.error(f"Error generating programming answers: {str(e)}")
            return [
                {
                    "question": q,
                    "detailed_answer": f"""This is a fundamental {language} concept.

**Key Points:**
- Study the official documentation
- Practice with hands-on examples  
- Understand the underlying concepts
- Consider performance implications

**Next Steps:**
Research this topic in detail and practice implementing examples to build your understanding.""",
                }
                for q in questions
            ]

    def _generate_leetcode_answers(self, questions: List[str]) -> List[Dict[str, str]]:
        """Generate detailed solutions for LeetCode-style questions."""
        system_prompt = """
        You are an expert algorithmic problem solver and coding interview coach. For each coding problem:
        1. Provide a complete, detailed solution with step-by-step explanation
        2. Include well-commented Python code
        3. Explain the algorithm approach and reasoning
        4. Analyze time and space complexity
        5. Discuss alternative approaches and optimizations
        6. Include edge cases and testing considerations

        Return in JSON format:
        [
            {
                "question": "original problem statement",
                "detailed_answer": "Comprehensive solution including problem analysis, multiple approaches, complete code with comments, complexity analysis, and testing strategies"
            }
        ]
        
        Make the detailed_answer very comprehensive with:
        - Problem breakdown and understanding
        - Multiple solution approaches (brute force, optimized, etc.)
        - Complete working code with detailed comments
        - Step-by-step algorithm explanation
        - Time and space complexity analysis
        - Edge cases to consider
        - Testing examples
        """

        try:
            response = self.llm.invoke(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(
                        content=f"Provide comprehensive solutions for these coding problems: {json.dumps(questions)}"
                    ),
                ]
            )

            try:
                return json.loads(response.content)
            except json.JSONDecodeError:
                return [
                    {
                        "question": q,
                        "detailed_answer": f"""**Problem Analysis:**
{q}

**Approach:**
1. Break down the problem into smaller components
2. Identify the core algorithm or data structure needed
3. Consider edge cases and constraints
4. Implement step by step

**Solution:**
```python
def solution(nums):
    '''
    Solve the problem step by step
    
    Args:
        nums: Input parameters
    
    Returns:
        Expected output
    '''
    # Step 1: Handle edge cases
    if not nums:
        return []
    
    # Step 2: Main algorithm logic
    result = []
    
    # Add your implementation here
    
    return result

# Test cases
def test_solution():
    # Test case 1
    assert solution([1, 2, 3]) == expected_result
    
    # Test case 2 - edge case
    assert solution([]) == []
    
    print("All tests passed!")
```

**Complexity Analysis:**
- Time Complexity: O(n) - analyze based on your implementation
- Space Complexity: O(1) - analyze based on your implementation

**Alternative Approaches:**
Consider different algorithms like:
1. Brute force approach
2. Optimized approach using specific data structures
3. Space-time trade-offs

**Key Insights:**
- Focus on understanding the problem requirements
- Think about edge cases early
- Consider multiple approaches before coding
- Write clean, readable code with comments""",
                    }
                    for q in questions
                ]
        except Exception as e:
            logger.error(f"Error generating LeetCode answers: {str(e)}")
            return [
                {
                    "question": q,
                    "detailed_answer": """**Problem-Solving Approach:**

1. **Understand the Problem:** Read carefully and identify inputs, outputs, and constraints
2. **Plan Your Solution:** Think through the algorithm before coding
3. **Implement:** Write clean, well-commented code
4. **Test:** Verify with multiple test cases including edge cases
5. **Optimize:** Consider time and space complexity improvements

**General Tips:**
- Start with a brute force solution if stuck
- Draw examples to visualize the problem
- Think about similar problems you've solved
- Practice common patterns (two pointers, sliding window, etc.)""",
                }
                for q in questions
            ]

    def _generate_code_review_answers(
        self, questions: List[str]
    ) -> List[Dict[str, str]]:
        """Generate detailed answers for code review questions."""
        system_prompt = """
        You are a senior software engineer and code review expert. For each code review question:
        1. Provide comprehensive guidance on code review best practices
        2. Include specific examples of what to look for
        3. Show code examples of good vs bad practices
        4. Explain the reasoning behind each recommendation
        5. Cover both technical and team collaboration aspects

        Return in JSON format:
        [
            {
                "question": "original question",
                "detailed_answer": "Comprehensive answer covering code review principles, specific examples with code snippets, best practices, and practical guidance"
            }
        ]
        
        Make the detailed_answer very comprehensive with:
        - Detailed explanation of code review principles
        - Specific code examples showing good vs bad practices
        - Practical tips for effective code reviews
        - Tools and techniques recommendations
        - Communication and collaboration advice
        """

        try:
            response = self.llm.invoke(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(
                        content=f"Provide comprehensive code review guidance for: {json.dumps(questions)}"
                    ),
                ]
            )

            try:
                return json.loads(response.content)
            except json.JSONDecodeError:
                return [
                    {
                        "question": q,
                        "detailed_answer": """**Code Review Best Practices:**

**1. Focus Areas:**
- **Readability:** Is the code easy to understand?
- **Functionality:** Does it work as intended?
- **Performance:** Are there efficiency concerns?
- **Security:** Any potential vulnerabilities?
- **Maintainability:** Easy to modify and extend?

**2. What to Look For:**
```python
# Bad Example:
def calc(x, y):
    return x * y + 10

# Good Example:
def calculate_total_price(quantity: int, unit_price: float) -> float:
    '''
    Calculate total price including $10 shipping fee
    
    Args:
        quantity: Number of items
        unit_price: Price per item
    
    Returns:
        Total price including shipping
    '''
    base_cost = quantity * unit_price
    shipping_fee = 10.0
    return base_cost + shipping_fee
```

**3. Review Checklist:**
- [ ] Clear variable and function names
- [ ] Proper error handling
- [ ] Adequate test coverage
- [ ] No code duplication
- [ ] Consistent formatting
- [ ] Security considerations
- [ ] Performance implications

**4. Communication Tips:**
- Be constructive and specific in feedback
- Suggest solutions, not just problems
- Acknowledge good practices
- Ask questions to understand context
- Focus on the code, not the person

**5. Tools and Techniques:**
- Use automated linting tools
- Set up CI/CD checks
- Review in small chunks
- Use collaborative review platforms
- Document team coding standards""",
                    }
                    for q in questions
                ]
        except Exception as e:
            logger.error(f"Error generating code review answers: {str(e)}")
            return [
                {
                    "question": q,
                    "detailed_answer": """**Code Review Guidelines:**

Focus on:
- Code readability and maintainability
- Proper error handling
- Security considerations
- Performance implications
- Testing coverage
- Documentation quality

Remember to provide constructive feedback and suggest improvements rather than just pointing out issues.""",
                }
                for q in questions
            ]

    def _generate_system_design_answers(
        self, questions: List[str]
    ) -> List[Dict[str, str]]:
        """Generate detailed answers for system design questions."""
        system_prompt = """
        You are a senior system architect and engineering leader. For each system design question:
        1. Provide a comprehensive system design approach
        2. Include architectural diagrams descriptions
        3. Discuss scalability, reliability, and performance considerations
        4. Cover data storage, caching, and distributed systems concepts
        5. Explain trade-offs and alternative approaches
        6. Include real-world examples and best practices

        Return in JSON format:
        [
            {
                "question": "original question",
                "detailed_answer": "Comprehensive system design answer including architecture overview, key components, scalability considerations, trade-offs, and implementation details"
            }
        ]
        
        Make the detailed_answer very comprehensive with:
        - Step-by-step system design approach
        - Key components and their interactions
        - Scalability and reliability strategies
        - Data storage and caching strategies
        - Performance considerations
        - Trade-offs and alternatives
        - Real-world implementation examples
        """

        try:
            response = self.llm.invoke(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(
                        content=f"Provide comprehensive system design guidance for: {json.dumps(questions)}"
                    ),
                ]
            )

            try:
                return json.loads(response.content)
            except json.JSONDecodeError:
                return [
                    {
                        "question": q,
                        "detailed_answer": f"""**System Design Approach for: {q}**

**1. Requirements Gathering:**
- **Functional Requirements:** What should the system do?
- **Non-Functional Requirements:** Performance, scalability, availability
- **Scale Estimation:** Users, requests/sec, data volume, storage needs

**2. High-Level Architecture:**
```
[Client] -> [Load Balancer] -> [API Gateway] -> [Services]
                                                     |
[Cache Layer] <- [Database Layer] <- [Message Queue]
```

**3. Key Components:**
- **Load Balancer:** Distribute traffic (NGINX, HAProxy)
- **API Gateway:** Authentication, rate limiting, routing
- **Application Servers:** Business logic (horizontally scalable)
- **Database:** Primary data storage (SQL/NoSQL based on needs)
- **Cache:** Fast data access (Redis, Memcached)
- **Message Queue:** Async processing (RabbitMQ, Apache Kafka)

**4. Scalability Strategies:**
- **Horizontal Scaling:** Add more servers
- **Database Sharding:** Distribute data across multiple DBs
- **Caching:** Multiple levels (browser, CDN, application, database)
- **Load Balancing:** Distribute requests efficiently
- **Microservices:** Break down into smaller, independent services

**5. Data Storage Considerations:**
- **SQL vs NoSQL:** Based on consistency and scalability needs
- **Replication:** Master-slave or master-master
- **Partitioning:** Horizontal (sharding) vs vertical
- **Backup and Recovery:** Regular backups, disaster recovery

**6. Performance Optimization:**
- **Caching Strategy:** What to cache and for how long
- **Database Indexing:** Speed up queries
- **CDN:** Static content delivery
- **Compression:** Reduce data transfer

**7. Reliability and Availability:**
- **Redundancy:** No single points of failure
- **Health Checks:** Monitor system health
- **Circuit Breaker:** Prevent cascade failures
- **Auto-scaling:** Handle traffic spikes

**8. Trade-offs to Consider:**
- **Consistency vs Availability (CAP Theorem)**
- **Cost vs Performance**
- **Complexity vs Maintainability**
- **Latency vs Throughput**

**9. Monitoring and Observability:**
- **Metrics:** System performance indicators
- **Logging:** Centralized log management
- **Alerting:** Proactive issue detection
- **Distributed Tracing:** Request flow tracking

**10. Security Considerations:**
- **Authentication & Authorization**
- **Data Encryption (in transit and at rest)**
- **Network Security (VPC, firewalls)**
- **Input Validation and Sanitization**""",
                    }
                    for q in questions
                ]
        except Exception as e:
            logger.error(f"Error generating system design answers: {str(e)}")
            return [
                {
                    "question": q,
                    "detailed_answer": """**System Design Framework:**

1. **Clarify Requirements:** Understand functional and non-functional requirements
2. **Estimate Scale:** Calculate users, requests, storage needs
3. **Design High-Level Architecture:** Components and their interactions
4. **Deep Dive:** Detailed design of key components
5. **Scale the Design:** Address bottlenecks and scaling strategies
6. **Consider Trade-offs:** Discuss alternatives and their implications

**Key Considerations:**
- Scalability and performance
- Reliability and availability  
- Consistency and data integrity
- Security and compliance
- Cost and operational complexity""",
                }
                for q in questions
            ]

    def _create_study_plan(self, state: StudyPlanState) -> StudyPlanState:
        """Create the final comprehensive study plan."""
        logger.info("Creating final study plan...")

        system_prompt = f"""
        You are a senior interview coach creating a personalized study plan. 
        Based on the candidate's profile:
        - Experience Level: {state['experience_level']}
        - Improvement Areas: {', '.join(state['improvement_areas'])}
        - Technical Skills: {', '.join(state['technical_skills'])}
        
        Create a structured study plan with timeframes and priorities.
        Consider their specific needs and improvement areas.
        """

        # Create timeline based on experience level
        timeline_weeks = {"entry": 4, "mid": 3, "senior": 2, "expert": 2}

        weeks = timeline_weeks.get(state["experience_level"], 3)

        study_plan = {
            "timeline": f"{weeks} weeks",
            "experience_level": state["experience_level"],
            "improvement_focus": state["improvement_areas"],
            "weekly_schedule": {
                "week_1": {
                    "focus": "Foundation & Best Practices",
                    "activities": [
                        "Review interview best practices",
                        "Practice STAR method for behavioral questions",
                        "Review resume and prepare examples",
                    ],
                },
                "week_2": {
                    "focus": "Technical Preparation",
                    "activities": [
                        "Practice programming language questions",
                        "Solve LeetCode problems (easy to medium)",
                        "Review system design basics (if applicable)",
                    ],
                },
            },
            "daily_practice": {
                "behavioral": "Practice 2-3 behavioral questions daily",
                "technical": "Solve 1-2 technical problems daily",
                "mock_interviews": "Schedule 1 mock interview per week",
            },
        }

        if weeks > 2:
            study_plan["weekly_schedule"]["week_3"] = {
                "focus": "Advanced Practice & Mock Interviews",
                "activities": [
                    "Practice harder technical problems",
                    "Conduct mock interviews",
                    "Review and refine responses",
                ],
            }

        if weeks > 3:
            study_plan["weekly_schedule"]["week_4"] = {
                "focus": "Final Preparation & Confidence Building",
                "activities": [
                    "Final mock interviews",
                    "Review company-specific information",
                    "Practice presentation skills",
                ],
            }

        state["study_plan"] = study_plan

        # Create final output
        final_output = {
            "candidate_profile": {
                "experience_level": state["experience_level"],
                "improvement_areas": state["improvement_areas"],
                "technical_skills": state["technical_skills"],
            },
            "study_plan": study_plan,
            "interview_best_practices": state["interview_practices"],
            "behavioral_questions": state["behavioral_questions"],
            "technical_questions": state["technical_questions"],
        }

        state["final_output"] = final_output
        return state

    def create_study_plan(self, resume_markdown: str) -> Dict[str, Any]:
        """Main method to create a study plan from resume."""
        if self.fast_mode:
            return self._create_study_plan_fast(resume_markdown)
        else:
            return self._create_study_plan_with_llm(resume_markdown)

    def _create_study_plan_fast(self, resume_content: str) -> Dict[str, Any]:
        """Create a comprehensive study plan quickly without API calls."""
        logger.info("Creating study plan using fast mode...")
        start_time = time.time()

        # Quick analysis
        analysis = self._analyze_resume_fast(resume_content)

        # Generate components
        best_practices = self._get_best_practices_fast(
            analysis["experience_level"], analysis["improvement_areas"]
        )

        behavioral_questions = self._get_behavioral_questions_fast(
            analysis["improvement_areas"]
        )
        technical_questions = self._get_technical_questions_fast(
            analysis["technical_skills"], analysis["experience_level"]
        )

        # Create study plan timeline
        timeline_weeks = {"entry": 4, "mid": 3, "senior": 2}
        weeks = timeline_weeks.get(analysis["experience_level"], 3)

        study_plan = {
            "timeline": f"{weeks} weeks",
            "experience_level": analysis["experience_level"],
            "improvement_focus": analysis["improvement_areas"],
            "weekly_schedule": {
                "week_1": {
                    "focus": "Foundation & Best Practices",
                    "activities": [
                        "Review interview best practices",
                        "Practice STAR method for behavioral questions",
                        "Review resume and prepare examples",
                    ],
                },
                "week_2": {
                    "focus": "Technical Preparation",
                    "activities": [
                        "Practice programming language questions",
                        "Solve coding problems (easy to medium)",
                        "Review system design basics (if applicable)",
                    ],
                },
            },
            "daily_practice": {
                "behavioral": "Practice 2-3 behavioral questions daily",
                "technical": "Solve 1-2 technical problems daily",
                "mock_interviews": "Schedule 1 mock interview per week",
            },
        }

        # Add week 3 for longer plans
        if weeks >= 3:
            study_plan["weekly_schedule"]["week_3"] = {
                "focus": "Advanced Practice & Mock Interviews",
                "activities": [
                    "Practice harder technical problems",
                    "Conduct mock interviews",
                    "Review and refine responses",
                ],
            }

        # Add week 4 for entry level
        if weeks >= 4:
            study_plan["weekly_schedule"]["week_4"] = {
                "focus": "Final Preparation & Confidence Building",
                "activities": [
                    "Final mock interviews",
                    "Review company-specific information",
                    "Practice presentation skills",
                ],
            }

        end_time = time.time()
        logger.info(
            f"Fast study plan creation completed in {end_time - start_time:.3f} seconds"
        )

        return {
            "candidate_profile": {
                "experience_level": analysis["experience_level"],
                "improvement_areas": analysis["improvement_areas"],
                "technical_skills": analysis["technical_skills"],
            },
            "study_plan": study_plan,
            "interview_best_practices": best_practices,
            "behavioral_questions": behavioral_questions,
            "technical_questions": technical_questions,
        }

    def _create_study_plan_with_llm(self, resume_markdown: str) -> Dict[str, Any]:
        """Create study plan using LLM API calls (original method)."""
        logger.info("Starting study plan creation with LLM...")

        initial_state = StudyPlanState(
            resume_content=resume_markdown,
            improvement_areas=[],
            technical_skills=[],
            experience_level="",
            study_plan={},
            interview_practices=[],
            behavioral_questions=[],
            technical_questions={},
            final_output={},
        )

        try:
            final_state = self.graph.invoke(initial_state)
            logger.info("Study plan creation completed successfully")
            return final_state["final_output"]

        except Exception as e:
            logger.error(f"Error creating study plan: {str(e)}")
            raise


# Convenience functions for direct usage
def create_study_plan(resume_markdown: str, fast_mode: bool = False) -> Dict[str, Any]:
    """
    Create a study plan from resume markdown.

    Args:
        resume_markdown: The resume content in markdown format
        fast_mode: If True, use fast keyword-based analysis (default: False)

    Returns:
        Dictionary containing the complete study plan
    """
    planner = InterviewStudyPlanner(fast_mode=fast_mode)
    return planner.create_study_plan(resume_markdown)


def create_fast_study_plan(resume_markdown: str) -> Dict[str, Any]:
    """
    Create a study plan quickly using keyword-based analysis.
    This is much faster than the LLM-based version but uses pattern matching.

    Args:
        resume_markdown: The resume content in markdown format

    Returns:
        Dictionary containing the complete study plan
    """
    return create_study_plan(resume_markdown, fast_mode=True)
