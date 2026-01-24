ATS Microservice – Breezy HR Integration (Serverless)
  Project Overview

This project is a serverless backend microservice built using Python and Serverless Framework that demonstrates integration with an Applicant Tracking System (ATS) — specifically Breezy HR.

The service exposes a unified REST API to:
-Fetch job openings
-Create candidates
-Assign candidates to jobs
-Track job applications

The application is designed to run locally using serverless-offline and is demonstrated using Postman / terminal.

Objective:
-To understand how ATS systems work
-To design a clean backend API that integrates with an ATS
-To demonstrate serverless architecture
-To handle real-world constraints like third-party API limitations

 Architecture Overview
Client (Postman / Terminal)
        |
        v
Serverless API (Python)
        |
        v
Breezy HR (Conceptual Integration)


⚠️ Note: Due to Breezy HR trial limitations (no API token exposure), ATS write operations are simulated while preserving the exact workflow and API contracts.

🧰 Tech Stack

-Backend: Python 3.x
-Framework: Serverless Framework
-Local Runtime: serverless-offline
-API Testing: Postman / curl
-Storage (Demo Only): JSON file (applications.json)

📁 Project Structure
ATSMicroService/
│
├── handler.py          # All API logic
├── serverless.yml      # Serverless configuration & routes
├── applications.json   # Temporary mock ATS storage
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

🚀 API Endpoints

1️⃣ Health Check
GET
/dev/health
Response
{
  "status": "Serverless service is running"
}

2️⃣ Fetch Jobs
GET
/dev/jobs
Description
Returns available job openings (mocked to represent Breezy HR jobs).

3️⃣ Create Candidate & Assign Job
POST
/dev/candidates
Request Body
{
  "name": "Sadath Khan",
  "email": "sadath@gmail.com",
  "phone": "9876543210",
  "resume_url": "https://example.com/resume.pdf",
  "job_id": "job_001"
}

Response
{
  "message": "Candidate created and assigned to job",
  "application": {
    "job_id": "job_001",
    "status": "APPLIED"
  }
}

4️⃣ Track Applications (with Pagination)
GET
/dev/applications?job_id=job_001&page=1&limit=5

Response
{
  "page": 1,
  "limit": 5,
  "total": 1,
  "data": [
    {
      "candidate_name": "sadath Khan",
      "job_id": "job_001",
      "status": "APPLIED"
    }
  ]
}

❗ Error Handling
-The API handles:
-Missing request body → 400 Bad Request
-Invalid JSON → 400 Bad Request
-Missing required fields → 400 Bad Request
-Internal failures → 500 Internal Server Error

Example:
{
  "error": "job_id is required"
}

📄 Pagination Support
Pagination is supported on the applications endpoint using:
page (default: 1)
limit (default: 10)
This mimics how real ATS APIs return large datasets.

⚠️ Breezy HR Integration Note (IMPORTANT)
Breezy HR does not expose API tokens in trial accounts.
Therefore:
-Job fetching is mocked
-Candidate creation & assignment are simulated
-Tracking data is stored temporarily in a JSON file
-In a production environment, all persistence and workflow would be handled directly by Breezy HR APIs without any local storage.

What Is NOT Included (and Why)

1. Real Breezy HR API Calls (Write Operations)
Not included because:
-Breezy HR trial accounts do not expose API tokens
-Candidate creation and job assignment endpoints are protected
How this is handled:
-ATS behavior is simulated
-API contracts and workflows are preserved
-The system can be switched to real APIs without redesign

2. Database     
Not included because:
-The assignment does not require building an ATS
-In real scenarios, ATS systems manage persistence
-Serverless functions are stateless by design
Demo workaround:
-A temporary JSON file is used only to demonstrate tracking

3. Authentication & Authorization
Not included because:
-Not part of the assignment requirements
-Focus is on ATS integration, not user management

4. Frontend / UI
Not included because:
-The requirement is backend-focused
-APIs are demonstrated using Postman / terminal
-UI can be added later as an enhancement

🧪 How to Run Locally
1️⃣ Install dependencies
npm install -g serverless
npm install
pip install -r requirements.txt

2️⃣ Start server
serverless offline

3️⃣ Test APIs
Use Postman
Or curl from terminal


✅ Conclusion
This project successfully demonstrates:
ATS integration concepts
Serverless backend design
Clean REST APIs
Error handling & pagination
Realistic hiring workflow simulation

👏 Author - Sadath Khan