## Project overview
Title: AI Interview Co-Pilot
Problem Statement:
  In the competitive software outsourcing industry, a high interview failure rate is a major bottleneck. This is often caused by a misalignment between our employees' CVs and the specific demands of a client's Job Description (JD), coupled with a lack of targeted interview practice. The manual process of reviewing CVs, identifying skill gaps, and preparing employees is time-consuming and inefficient.
  The Challenge:
  Your challenge is to design and build an AI-powered platform that acts as an "Interview Co-Pilot." This tool will streamline the preparation process to dramatically increase the interview success rate for our employees.
  Key Features to Consider:
  CV-JD Gap Analysis: Automatically parse an employee's CV and a client's JD to highlight matching skills, identify gaps, and suggest optimizations for the CV.
  Personalized Study Plan: Based on the identified gaps, generate a targeted learning plan with recommended resources to upskill the employee.
  AI-Powered Mock Interviews: Simulate a realistic interview experience with relevant technical and behavioral questions, providing instant feedback on answers, clarity, and confidence.
  Success Metric: The winning solution will be judged on its ability to effectively reduce preparation time, accurately identify skill gaps, and provide a realistic and helpful mock interview experience.
##Techstack:
- Backend: Python, flask, swagger
- Persistent: PostgreSQL

##Features:
- Interview Project Management - CRUD
- Project Name
- Job Description
- Customer Information
## Databases:
{
  "resume": {
    "id": "string-uuid",
    "first_name": string,
    "last_name": string,
  },
  "education": {
    "resumeId": "string-uuid",
    "school": "School Name",
    "degree": "Degree Name",
    "major": "Major Field",
    "start": "YYYY-MM-DDTHH:MM:SS",
    "end": "YYYY-MM-DDTHH:MM:SS",
    "grade": "GPA or Grade",
    "completeDegree": true,
    "id": "string-uuid",
    "createdOn": "YYYY-MM-DDTHH:MM:SS.ssssss",
    "createdBy": "string-uuid",
    "modifiedOn": "YYYY-MM-DDTHH:MM:SS.ssssss",
    "modifiedBy": "string-uuid"
  },
  "certificates": [
    {
      "resumeId": "string-uuid",
      "certificate": "Certificate Name",
      "certificateAuthority": "Authority Name or null",
      "notExpired": true,
      "issueDate": "YYYY-MM-DDTHH:MM:SS",
      "expirationDate": "YYYY-MM-DDTHH:MM:SS or null",
      "score": "Score or null",
      "licenseNo": "License Number or null",
      "certificateUrl": "URL or null",
      "foreignLanguage": "Language or null",
      "subject": "Subject or null",
      "isCTCSponsor": false,
      "grade": "Grade or null",
      "certificateCatalogId": "string-uuid",
      "providerId": "string-uuid",
      "provider": "Provider Name",
      "fieldId": "string-uuid",
      "field": "Field Name",
      "subFieldId": "string-uuid",
      "subField": "Sub Field Name",
      "levelId": "string-uuid or null",
      "level": "Level Name",
      "status": 0,
      "attendance": true,
      "fileName": "filename.pdf or null",
      "isSynced": false,
      "isEducation": false,
      "techType": "Tech Type or null",
      "rejectReason": "Reason or null",
      "isNotHasLicenseNumber": false,
      "id": "string-uuid",
      "createdOn": "YYYY-MM-DDTHH:MM:SS.ssssss",
      "createdBy": "string-uuid",
      "modifiedOn": "YYYY-MM-DDTHH:MM:SS.ssssss or null",
      "modifiedBy": "string-uuid or null"
    }
  ],
  "languages": [
    {
      "resumeId": "string-uuid",
      "proficiency": 0,
      "language": {
        "name": "Language Name",
        "id": "string-uuid",
        "createdOn": "YYYY-MM-DDTHH:MM:SS.ssssss",
        "createdBy": "string-uuid",
        "modifiedOn": "YYYY-MM-DDTHH:MM:SS.ssssss",
        "modifiedBy": "string-uuid"
      },
      "id": "string-uuid",
      "createdOn": "YYYY-MM-DDTHH:MM:SS.ssssss",
      "createdBy": "string-uuid",
      "modifiedOn": "YYYY-MM-DDTHH:MM:SS.ssssss",
      "modifiedBy": "string-uuid"
    }
  ],
  "domain": [
    {
      "name": "Domain Name",
      "year": 0,
      "month": 0,
      "resumeId": "string-uuid",
      "id": "string-uuid",
      "createdOn": "YYYY-MM-DDTHH:MM:SS.ssssss",
      "createdBy": "string-uuid",
      "modifiedOn": "YYYY-MM-DDTHH:MM:SS.ssssss",
      "modifiedBy": "string-uuid"
    }
  ],
  "projects": [
    {
      "resumeId": "string-uuid",
      "resumeProjectId": "string-uuid",
      "projectId": "string-uuid",
      "name": "Project Name",
      "projectKey": "Project Key",
      "projectCode": "Project Code",
      "projectRank": "A/B/C",
      "projectLead": "Lead Name or ID",
      "projectCategory": "Development/Maintenance",
      "customerCode": "Customer Code",
      "contractType": "T&M/Fixed Price",
      "url": "Project URL",
      "company": "Company Name",
      "type": "Internal/External",
      "teamSize": 0,
      "searchSkill": 0,
      "technology": [
        "Tech1",
        "Tech2"
      ],
      "projectDescription": "Short project description.",
      "groupname": "Group Name",
      "status": "On-going/Closed",
      "domain": "Domain Name",
      "startDate": "YYYY-MM-DDTHH:MM:SS",
      "endDate": "YYYY-MM-DDTHH:MM:SS",
      "painPoins": "Pain Points or null",
      "keyFindings": "Key Findings or null",
      "workingProcess": "Working Process or null",
      "responsibility": "Responsibility Description",
      "technologyByPM": "Tech by PM or null",
      "descriptionByPM": "Description by PM or null",
      "isUpdateTeam": false,
      "applyIncompleted": false,
      "skill": "Skill Name",
      "skillCode": "Skill Code or null",
      "seniority": "Seniority Level or null",
      "projectRoles": [],
      "projectSkills": [],
      "projectJobs": []
    }
  ],
  "professionalSkills": [
    {
      "id": "string-uuid",
      "resumeId": "string-uuid",
      "jobTitleName": "Skill/Job Title",
      "experienceMonth": 0,
      "experienceYear": 0,
      "jobFillByUser": "string or null",
      "isMainSkill": false,
      "projectInfo": []
    }
  ]
}
