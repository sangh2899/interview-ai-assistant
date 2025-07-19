# Interview Co-Pilot API

A Flask REST API for managing interview projects and resumes. This API provides CRUD operations for resumes, education, certificates, languages, domains, projects, and professional skills.

## Tech Stack

- Backend: Python, Flask, Flask-RESTX (Swagger)
- Database: PostgreSQL
- ORM: SQLAlchemy
- Migration: Flask-Migrate

## Features

- Resume Management (CRUD) with comprehensive data aggregation
- Education Records Management
- Certificate Management
- Language Skills Management
- Domain Experience Management
- Project Management
- Professional Skills Management
- Complete Resume Data API (all related data in nested structure)
- Swagger API Documentation

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip

### Installation

1. **Quick Setup (Recommended)**:
```bash
./setup.sh
```

2. **Manual Setup**:

Clone the repository:
```bash
git clone <repository-url>
cd hackathon-api
```

Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Setup PostgreSQL database:
- Create a PostgreSQL database named `interview_api`
- Update the `.env` file with your database credentials

Configure environment variables:
```bash
cp .env .env.local
# Edit .env.local with your database credentials
```

Initialize the database:
```bash
export FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

3. **Docker Setup**:
```bash
docker-compose up --build
```

### Running the Application

**Development Mode**:
```bash
source venv/bin/activate  # If not already activated
python run.py
```

**With Docker**:
```bash
docker-compose up
```

The API will be available at `http://localhost:5000` and Swagger documentation at `http://localhost:5000/swagger/`

### Seeding the Database

To populate the database with sample data:
```bash
python seed_data.py
```

Or using the CLI command:
```bash
python run.py seed-db
```

This will create sample data for all entities including:
- 5 resumes with complete contact information
- Education records from various universities
- Professional certificates (AWS, Google Cloud, etc.)
- Multiple language skills
- Domain experiences across different industries
- Complex project information
- Professional skills with experience levels

### Testing the API

Run the test script to verify everything is working:
```bash
python test_api.py
```

### Comprehensive Resume Data

The API provides a special endpoint `/resumes/{id}/full` that returns all related data for a resume in a nested JSON structure. This includes:

- Resume basic information (name, email, phone, summary)
- All education records
- All certificates with complete details
- All language skills with language information
- All domain experiences
- All projects with comprehensive details
- All professional skills

Example response structure:
```json
{
  "id": "resume-uuid",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-0101",
  "summary": "Senior Software Engineer...",
  "educations": [...],
  "certificates": [...],
  "languages": [...],
  "domains": [...],
  "projects": [...],
  "professional_skills": [...]
}
```

## API Endpoints

### Resumes
- `GET /resumes/` - Get all resumes
- `POST /resumes/` - Create a new resume
- `GET /resumes/{id}` - Get a specific resume
- `PUT /resumes/{id}` - Update a specific resume
- `DELETE /resumes/{id}` - Delete a specific resume
- `GET /resumes/{id}/full` - Get complete resume data with all related information in nested structure

### Education
- `GET /education/` - Get all education records
- `POST /education/` - Create a new education record
- `GET /education/{id}` - Get a specific education record
- `PUT /education/{id}` - Update a specific education record
- `DELETE /education/{id}` - Delete a specific education record
- `GET /education/resume/{resume_id}` - Get all education records for a resume

### Certificates
- `GET /certificates/` - Get all certificates
- `POST /certificates/` - Create a new certificate
- `GET /certificates/{id}` - Get a specific certificate
- `PUT /certificates/{id}` - Update a specific certificate
- `DELETE /certificates/{id}` - Delete a specific certificate
- `GET /certificates/resume/{resume_id}` - Get all certificates for a resume

### Languages
- `GET /languages/` - Get all languages
- `POST /languages/` - Create a new language
- `GET /languages/{id}` - Get a specific language
- `PUT /languages/{id}` - Update a specific language
- `DELETE /languages/{id}` - Delete a specific language
- `GET /languages/skills` - Get all language skills
- `POST /languages/skills` - Create a new language skill
- `GET /languages/skills/{id}` - Get a specific language skill
- `PUT /languages/skills/{id}` - Update a specific language skill
- `DELETE /languages/skills/{id}` - Delete a specific language skill
- `GET /languages/skills/resume/{resume_id}` - Get all language skills for a resume

### Domains
- `GET /domains/` - Get all domains
- `POST /domains/` - Create a new domain
- `GET /domains/{id}` - Get a specific domain
- `PUT /domains/{id}` - Update a specific domain
- `DELETE /domains/{id}` - Delete a specific domain
- `GET /domains/resume/{resume_id}` - Get all domains for a resume

### Projects
- `GET /projects/` - Get all projects
- `POST /projects/` - Create a new project
- `GET /projects/{id}` - Get a specific project
- `PUT /projects/{id}` - Update a specific project
- `DELETE /projects/{id}` - Delete a specific project
- `GET /projects/resume/{resume_id}` - Get all projects for a resume

### Professional Skills
- `GET /professional-skills/` - Get all professional skills
- `POST /professional-skills/` - Create a new professional skill
- `GET /professional-skills/{id}` - Get a specific professional skill
- `PUT /professional-skills/{id}` - Update a specific professional skill
- `DELETE /professional-skills/{id}` - Delete a specific professional skill
- `GET /professional-skills/resume/{resume_id}` - Get all professional skills for a resume

## Database Schema

The API follows the database schema defined in the project requirements with the following main entities:

- Resume (first_name, last_name, email, phone, summary)
- Education (school, degree, major, dates, grade)
- Certificate (certificate details, authorities, dates, scores)
- Language & LanguageSkill (language proficiency mapping)
- Domain (domain experience with years/months)
- Project (comprehensive project information)
- ProfessionalSkill (job titles and experience levels)

## Development

To run in development mode:
```bash
export FLASK_ENV=development
python run.py
```

## Notes

- All IDs are UUIDs
- Timestamps are automatically managed
- Foreign key relationships are properly configured with cascading deletes
- API includes comprehensive Swagger documentation
- Error handling for 404 cases included
