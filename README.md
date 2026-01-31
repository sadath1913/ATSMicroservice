ATS Integration Microservice – Zoho Recruit (Serverless)
📌 Project Overview

This project is a serverless backend microservice built using Python and the Serverless Framework that demonstrates integration with a real Applicant Tracking System (ATS) — Zoho Recruit.

The service exposes a unified REST API layer that abstracts ATS-specific complexity and provides standardized endpoints to:

Fetch job openings

Create candidates
Assign candidates to jobs (applications)
Track applications for a given job
The service runs locally using serverless-offline and can be tested using Postman or curl.

🎯 Objective

Understand how real ATS systems work
Design a clean backend API that integrates with an external ATS
Demonstrate serverless architecture using AWS Lambda
Handle real-world concerns such as:
OAuth-based authentication
External API integration
Error handling
Pagination
Secure credential management

🏗️ Architecture Overview
Client (Postman / curl / UI)
        |
        v
Serverless API (Python – AWS Lambda)
        |
        v
Zoho Recruit ATS (External System)


The microservice acts as an integration layer, translating Zoho Recruit data into a standardized internal format.

🧰 Tech Stack

Backend: Python 3.x
Framework: Serverless Framework
Cloud Runtime: AWS Lambda
Local Runtime: serverless-offline
ATS: Zoho Recruit
API Testing: Postman / curl

📁 Project Structure
ATSMicroService/
│
├── handler.py          # All API logic & ATS integration
├── serverless.yml      # Serverless configuration & routes
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

🔐 Authentication & Configuration (IMPORTANT)
OAuth Access Token
Zoho Recruit APIs are secured using OAuth 2.0.

Steps followed:
Create an application in Zoho API Console
Generate OAuth access token
Pass the token in every API request using:
Authorization: Zoho-oauthtoken <ACCESS_TOKEN>
The access token is never hard-coded in the source code.
Base URL
Zoho provides region-specific API domains.

For India region:
https://www.zohoapis.in
Environment Variables Used
All sensitive configuration is handled using environment variables, as required by the assignment.

Variable	Description
ATS_API_TOKEN	=Zoho Recruit OAuth access token(1000.6a1547dc5b170c6f1058b7cec19354f8.63293e9647411671ccef9bfb1fcd7a7)
ATS_BASE_URL	=Zoho API base URL("https://www.zohoapis.in")
ATS_PORTAL_ID	=Zoho Recruit portal (organization) ID (60000422501)

In code:

ATS_API_TOKEN = os.getenv("ATS_API_TOKEN")
ATS_BASE_URL = os.getenv("ATS_BASE_URL")
ATS_PORTAL_ID = os.getenv("ATS_PORTAL_ID")


This ensures:

Secure handling of secrets
Easy configuration changes
Production-ready design

🚀 API Endpoints
1️⃣ Health Check

GET
/dev/health
Response
{
  "status": "ATS microservice running"
}

2️⃣ Fetch Jobs from ATS
GET
/dev/jobs
Description
Fetches job openings from Zoho Recruit and returns them in a standardized format.
Response Format
{
  "id": "string",
  "title": "string",
  "location": "string",
  "status": "OPEN",
  "external_url": "string"
}

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

Workflow
Candidate is created in Zoho Recruit
Candidate is attached to the specified job
An application (pipeline entry) is created
Response
{
  "message": "Candidate created and assigned to job successfully",
  "candidate_id": "string"
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
      "id": "string",
      "candidate_name": "Sadath Khan",
      "email": "sadath@gmail.com",
      "status": "APPLIED"
    }
  ]
}

❗ Error Handling

The service returns clean JSON errors for all failure scenarios:
Missing request body → 400 Bad Request
Invalid JSON → 400 Bad Request
Missing required fields → 400 Bad Request
ATS/API failures → 500 Internal Server Error
Example
{
  "error": "job_id is required"
}

📄 Pagination Support

Pagination is implemented on the applications endpoint using:
page (default: 1)
limit (default: 10)
This mimics how real ATS APIs handle large datasets.

🔗 Zoho Recruit Integration Details
Free Trial / Sandbox Setup
Sign up for Zoho Recruit
Enable sample data
Create an application in Zoho API Console
Generate OAuth access token
Set required environment variables
Authentication
OAuth 2.0
Token passed via request headers
No credentials stored in source code
⚠️ External ATS Integration Note

The codebase implements real Zoho Recruit API integration using OAuth authentication and official endpoints.
During evaluation, API execution may depend on:
Network availability
Token validity
ATS account state

However, the architecture, API contracts, workflows, and logic fully represent a real-world ATS integration and can be executed in production without refactoring.

❌ What Is NOT Included (and Why)
1️⃣ Database
ATS systems manage persistence
Serverless functions are stateless
No database required for this assignment

2️⃣ Authentication & Authorization (Users)
Not part of assignment scope
Focus is ATS integration, not user management

3️⃣ Frontend / UI
Backend-focused task
APIs tested using Postman / curl
UI can be added as an enhancement

🧪 How to Run Locally
1️⃣ Install dependencies
npm install -g serverless
npm install
pip install -r requirements.txt

2️⃣ Set environment variables
setx ATS_API_TOKEN "your_zoho_access_token"
setx ATS_BASE_URL "https://www.zohoapis.in"
setx ATS_PORTAL_ID "your_portal_id"


Restart terminal after setting variables.

3️⃣ Start server
serverless offline

4️⃣ Test APIs
Postman

✅ Conclusion
This project successfully demonstrates:
Real-world ATS integration using Zoho Recruit
Serverless backend design with AWS Lambda
Secure OAuth-based authentication
Clean REST APIs with standardized responses
Error handling and pagination
Complete hiring workflow:
Jobs → Candidates → Applications
