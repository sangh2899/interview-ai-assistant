"""
Interview Question Bank
Contains questions across different categories for interview preparation.
"""

INTERVIEW_QUESTIONS = {
    "programming_languages": {
        "python": [
            "Explain the difference between list and tuple in Python.",
            "What is a decorator in Python? Provide an example.",
            "How does Python's garbage collection work?",
            "Explain the concept of generators and when to use them.",
            "What are context managers in Python?",
            "Difference between shallow copy and deep copy.",
            "Explain the Global Interpreter Lock (GIL) in Python.",
            "What are metaclasses in Python?",
            "How do you handle exceptions in Python?",
            "Explain the difference between @staticmethod and @classmethod.",
        ],
        "javascript": [
            "Explain the concept of closures in JavaScript.",
            "What is the difference between let, const, and var?",
            "How does prototypal inheritance work in JavaScript?",
            "Explain the event loop in JavaScript.",
            "What are Promises and how do they work?",
            "Difference between == and === in JavaScript.",
            "What is hoisting in JavaScript?",
            "Explain the concept of this in JavaScript.",
            "What are arrow functions and how do they differ from regular functions?",
            "How does async/await work in JavaScript?",
        ],
        "java": [
            "Explain the difference between abstract classes and interfaces.",
            "What is the purpose of the 'final' keyword in Java?",
            "How does garbage collection work in Java?",
            "Explain the concept of polymorphism in Java.",
            "What are the different types of inheritance in Java?",
            "Difference between ArrayList and LinkedList.",
            "What is the difference between checked and unchecked exceptions?",
            "Explain the concept of multithreading in Java.",
            "What are generics in Java?",
            "How does the HashMap work internally?",
        ],
        "cpp": [
            "Explain the difference between malloc and new in C++.",
            "What are virtual functions and why are they used?",
            "Difference between pass by value and pass by reference.",
            "What is RAII in C++?",
            "Explain the concept of smart pointers.",
            "What are the differences between struct and class in C++?",
            "How does multiple inheritance work in C++?",
            "What is the purpose of const keyword in C++?",
            "Explain template metaprogramming.",
            "What is the difference between stack and heap allocation?",
        ],
    },
    "leetcode": [
        "Two Sum - Given an array of integers, return indices of two numbers that add up to a target.",
        "Reverse Linked List - Reverse a singly linked list iteratively and recursively.",
        "Valid Parentheses - Given a string containing just parentheses, determine if the input string is valid.",
        "Merge Two Sorted Lists - Merge two sorted linked lists and return as a new sorted list.",
        "Maximum Subarray - Find the contiguous subarray with the largest sum.",
        "Climbing Stairs - Count the number of distinct ways to climb n stairs.",
        "Binary Tree Inorder Traversal - Return the inorder traversal of a binary tree.",
        "Symmetric Tree - Check whether a binary tree is a mirror of itself.",
        "Maximum Depth of Binary Tree - Find the maximum depth of a binary tree.",
        "Same Tree - Check if two binary trees are the same.",
        "Pascal's Triangle - Generate the first numRows of Pascal's triangle.",
        "Best Time to Buy and Sell Stock - Find the maximum profit from buying and selling stock.",
        "Valid Palindrome - Check if a string is a palindrome considering only alphanumeric characters.",
        "Single Number - Find the element that appears only once in an array.",
        "Linked List Cycle - Determine if a linked list has a cycle.",
        "Min Stack - Design a stack that supports push, pop, top, and retrieving minimum element.",
        "Intersection of Two Linked Lists - Find the node at which two singly linked lists intersect.",
        "Excel Sheet Column Title - Convert a column number to its corresponding Excel column title.",
        "Majority Element - Find the majority element in an array.",
        "Factorial Trailing Zeroes - Count the number of trailing zeroes in n!.",
    ],
    "code_review": [
        "How would you optimize this O(n²) algorithm to O(n log n)?",
        "What potential security vulnerabilities do you see in this code?",
        "How would you refactor this function to make it more readable?",
        "What design patterns would you apply to improve this code structure?",
        "How would you handle error cases in this implementation?",
        "What would you do to make this code more testable?",
        "How would you improve the performance of this database query?",
        "What are the potential race conditions in this concurrent code?",
        "How would you implement proper logging and monitoring for this service?",
        "What steps would you take to make this code more maintainable?",
    ],
    "system_design": [
        "Design a URL shortening service like bit.ly",
        "Design a chat application like WhatsApp",
        "Design a social media feed like Twitter",
        "Design a video streaming service like YouTube",
        "Design a ride-sharing service like Uber",
        "Design a search engine like Google",
        "Design a distributed cache system",
        "Design a notification system",
        "Design a rate limiting system",
        "Design a file storage system like Dropbox",
    ],
    "behavioral": [
        "Tell me about a time when you had to work with a difficult team member.",
        "Describe a situation where you had to meet a tight deadline.",
        "Tell me about a time when you failed at something. What did you learn?",
        "Describe a project you're particularly proud of.",
        "How do you handle disagreements with your manager?",
        "Tell me about a time when you had to learn a new technology quickly.",
        "Describe a situation where you had to make a difficult decision.",
        "How do you prioritize your work when you have multiple deadlines?",
        "Tell me about a time when you received constructive criticism.",
        "Describe a situation where you had to work with limited resources.",
    ],
    "leadership": [
        "Describe your leadership style.",
        "How do you motivate team members who are struggling?",
        "Tell me about a time when you had to resolve a conflict within your team.",
        "How do you handle team members who consistently miss deadlines?",
        "Describe how you would onboard a new team member.",
        "How do you ensure effective communication within your team?",
        "Tell me about a time when you had to make an unpopular decision.",
        "How do you handle performance reviews and feedback?",
        "Describe your approach to delegating tasks.",
        "How do you build trust within your team?",
    ],
    "soft_skills": [
        "How do you stay updated with the latest technology trends?",
        "Describe your approach to problem-solving.",
        "How do you handle stress and pressure at work?",
        "What motivates you in your career?",
        "How do you ensure work-life balance?",
        "Describe a time when you had to explain a complex technical concept to a non-technical person.",
        "How do you handle feedback and criticism?",
        "What are your career goals for the next 5 years?",
        "How do you approach continuous learning and skill development?",
        "Describe your ideal work environment.",
    ],
}

BEST_PRACTICES = {
    "general": [
        "Research the company and role thoroughly before the interview",
        "Prepare specific examples using the STAR method (Situation, Task, Action, Result)",
        "Practice coding problems on a whiteboard or online platform",
        "Prepare thoughtful questions to ask the interviewer",
        "Review your resume and be ready to discuss any experience mentioned",
        "Dress appropriately for the company culture",
        "Arrive 10-15 minutes early",
        "Bring multiple copies of your resume",
        "Follow up with a thank-you email within 24 hours",
    ],
    "technical": [
        "Think out loud while solving problems",
        "Ask clarifying questions before starting to code",
        "Start with a brute force solution, then optimize",
        "Write clean, readable code with proper variable names",
        "Test your solution with edge cases",
        "Explain your approach and time/space complexity",
        "Be honest about what you don't know",
        "Show your problem-solving process",
        "Practice with the tools you'll use in the interview",
    ],
    "behavioral": [
        "Use the STAR method for structured responses",
        "Be honest and authentic in your answers",
        "Focus on your role and contributions in team situations",
        "Show learning and growth from challenges",
        "Demonstrate self-awareness and reflection",
        "Prepare examples that showcase different skills",
        "Practice storytelling to make your examples engaging",
        "Be specific with metrics and outcomes when possible",
    ],
}


def get_questions_by_category(category: str, subcategory: str = None, count: int = 5):
    """Get interview questions by category and optional subcategory."""
    if category not in INTERVIEW_QUESTIONS:
        return []

    if subcategory and isinstance(INTERVIEW_QUESTIONS[category], dict):
        if subcategory in INTERVIEW_QUESTIONS[category]:
            questions = INTERVIEW_QUESTIONS[category][subcategory]
        else:
            return []
    else:
        questions = INTERVIEW_QUESTIONS[category]

    # Return up to 'count' questions
    return questions[:count] if len(questions) > count else questions


def get_best_practices(category: str = "general"):
    """Get best practices for interviews."""
    return BEST_PRACTICES.get(category, [])


def get_all_categories():
    """Get all available question categories."""
    return list(INTERVIEW_QUESTIONS.keys())


def get_subcategories(category: str):
    """Get subcategories for a given category."""
    if category in INTERVIEW_QUESTIONS and isinstance(
        INTERVIEW_QUESTIONS[category], dict
    ):
        return list(INTERVIEW_QUESTIONS[category].keys())
    return []
