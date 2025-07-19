# AI Interview Copilot Agent

A voice-powered AI interviewer that conducts technical interviews using LiveKit, LangGraph workflows, and RAG (Retrieval-Augmented Generation) for intelligent question selection and candidate evaluation.

## 🎯 Features

- **Voice-Powered Interviews**: Real-time voice interaction using LiveKit's STT/TTS
- **Intelligent Question Selection**: RAG-based question selection from curated question banks
- **Dynamic Interview Flow**: LangGraph workflow for adaptive interview progression
- **Real-time Transcription**: Complete conversation recording and transcription
- **Interview Analysis**: AI-powered candidate evaluation and recommendations
- **Resume & Job Matching**: Automatic interview plan creation based on resume and job requirements

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LiveKit       │    │   LangGraph     │    │   RAG System    │
│   Agent         │◄──►│   Workflow      │◄──►│   (ChromaDB)    │
│                 │    │                 │    │                 │
│ • Voice I/O     │    │ • Interview     │    │ • Resumes       │
│ • STT/TTS       │    │   Planning      │    │ • Job Descrip.  │
│ • Recording     │    │ • Question Flow │    │ • Question Bank │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Components

### 1. Mock Data Generator (`mock_data_generator.py`)
- Generates sample resumes, job descriptions, and question banks
- Creates realistic test data for different roles (Software Engineer, Data Scientist)
- Categorized questions (Technical, Behavioral, Project Deep Dive)

### 2. RAG System (`rag_system.py`)
- ChromaDB vector database for storing interview-related data
- OpenAI embeddings for semantic search
- Smart resume-to-job matching
- Question retrieval by category and relevance

### 3. Interview Workflow (`interview_workflow.py`)
- LangGraph-powered interview state management
- Dynamic interview plan creation
- Intelligent follow-up question generation
- Real-time answer analysis and scoring

### 4. Interview Agent (`interview_agent.py`)
- LiveKit agent for voice interactions
- Integration with RAG and workflow systems
- Real-time transcription and recording
- Interview session management

### 5. Setup & Test Script (`setup_and_test.py`)
- Automated system setup and validation
- Component testing and verification
- Environment configuration assistance

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Required API Keys**:
   - OpenAI API key (for LLM and embeddings)
   - LiveKit credentials (URL, API key, API secret)
   - Cartesia API key (for TTS)
   - Deepgram API key (for STT)
   - Tavily API key (optional, for web search)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-interview-copilot-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup and test**:
   ```bash
   python setup_and_test.py
   ```
   
   This will:
   - Check dependencies
   - Create `.env.example` template
   - Generate mock data
   - Test all components

4. **Configure environment**:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API keys
   ```

5. **Test the system**:
   ```bash
   python setup_and_test.py
   ```

### Running the Interview Agent

1. **Start the agent**:
   ```bash
   python interview_agent.py dev
   ```

2. **Connect a client**:
   - Use LiveKit's sandbox or any compatible frontend
   - Connect to the room and start speaking

## 🔧 Configuration

### Environment Variables

Create `.env.local` with the following variables:

```env
# LiveKit Configuration
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# Voice Services
CARTESIA_API_KEY=your-cartesia-api-key
DEEPGRAM_API_KEY=your-deepgram-api-key

# Optional: Web Search
TAVILY_API_KEY=your-tavily-api-key
```

### Customization

#### Adding New Question Categories

Edit `mock_data_generator.py` to add new question categories:

```python
QuestionBank(
    category="Your New Category",
    difficulty="Medium",
    questions=[
        {
            "question": "Your question here?",
            "follow_up": "Follow-up question?"
        }
    ]
)
```

#### Modifying Interview Flow

Update `interview_workflow.py` to customize:
- Interview duration
- Question selection logic
- Follow-up question criteria
- Scoring algorithms

## 📊 Output & Results

### Interview Results Structure

```
interview_results/
├── interview_John_Smith_1704067200/
│   ├── transcription.json          # Complete conversation log
│   ├── interview_analysis.json     # Interview plan and evaluation
│   └── interview_audio.wav         # Audio recording (if available)
```

### Transcription Format

```json
{
  "interview_id": "interview_John_Smith_1704067200",
  "candidate_name": "John Smith",
  "start_time": "2024-01-01T10:00:00",
  "end_time": "2024-01-01T10:30:00",
  "transcription": [
    {
      "timestamp": "2024-01-01T10:00:00",
      "speaker": "interviewer",
      "message": "Hello John! Thank you for joining us today...",
      "type": "question"
    },
    {
      "timestamp": "2024-01-01T10:00:30",
      "speaker": "candidate", 
      "message": "Thank you for having me...",
      "type": "answer"
    }
  ]
}
```

### Interview Analysis

```json
{
  "interview_summary": {
    "overall_assessment": "Strong technical candidate...",
    "technical_competency": "Advanced",
    "communication_skills": "Excellent",
    "recommendation": "hire",
    "key_highlights": [...],
    "areas_of_concern": [...]
  },
  "questions_and_answers": [
    {
      "category": "Technical - Software Engineering",
      "question": "Explain the difference between SQL and NoSQL databases...",
      "answer": "SQL databases are relational...",
      "follow_up": "Can you give me a specific example...",
      "asked": true,
      "follow_up_asked": true
    }
  ]
}
```

## 🧪 Testing

### Individual Component Testing

```bash
# Test RAG system
python rag_system.py

# Test interview workflow
python interview_workflow.py

# Generate fresh mock data
python mock_data_generator.py

# Run comprehensive tests
python setup_and_test.py
```

### Test Interview Flow

1. **Start the agent in console mode**:
   ```bash
   python interview_agent.py console
   ```

2. **Type responses** to test the workflow without voice

3. **Check generated results** in `interview_results/` directory

## 🔍 Troubleshooting

### Common Issues

1. **Dependencies not installed**:
   ```bash
   pip install -r requirements.txt
   ```

2. **API keys not configured**:
   - Check `.env.local` file exists
   - Verify all required API keys are set

3. **ChromaDB permissions**:
   ```bash
   # Clean ChromaDB directory if corrupted
   rm -rf ./chroma_db
   python setup_and_test.py
   ```

4. **LiveKit connection issues**:
   - Verify LIVEKIT_URL is correct
   - Check API key/secret permissions
   - Ensure network connectivity

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🛠️ Development

### Architecture Decisions

- **KISS Principle**: Simple, modular design without over-engineering
- **Async/Await**: For real-time voice processing
- **State Management**: LangGraph for complex interview flow
- **Vector Search**: ChromaDB for efficient semantic search
- **Voice Quality**: LiveKit for professional-grade audio

### Extending the System

1. **Add new question types**: Modify `mock_data_generator.py`
2. **Customize interview logic**: Update `interview_workflow.py`
3. **Integrate new voice services**: Extend `interview_agent.py`
4. **Add new data sources**: Enhance `rag_system.py`

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📧 Support

For issues and questions:
- Check the troubleshooting section
- Review component logs
- Test individual components
- Open an issue with detailed error information

---

**Built with**: LiveKit Agents, LangGraph, LangChain, ChromaDB, OpenAI, Cartesia, Deepgram 