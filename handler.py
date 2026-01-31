import json
import os
import requests


# Environment Variables

ATS_API_TOKEN = os.getenv("ATS_API_TOKEN")
ATS_BASE_URL = os.getenv("ATS_BASE_URL")
ATS_PORTAL_ID = os.getenv("ATS_PORTAL_ID")

HEADERS = {
    "Authorization": f"Zoho-oauthtoken {ATS_API_TOKEN}",
    "Content-Type": "application/json"
}


# Health Check

def health_check(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({"status": "ATS microservice running"})
    }


# GET /jobs

def get_jobs(event, context):
    try:
        url = f"{ATS_BASE_URL}/recruit/v2/JobOpenings"
        params = {
            "portal_id": ATS_PORTAL_ID,
            "fields": "Job_Title,City,State,Country",
            "page": 1,
            "per_page": 20
        }

        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code != 200:
            return {
                "statusCode": response.status_code,
                "body": json.dumps({"error": "Failed to fetch jobs from ATS"})
            }

        jobs = []
        for job in response.json().get("data", []):
            jobs.append({
                "id": job.get("id"),
                "title": job.get("Job_Title"),
                "location": job.get("City"),
                "status": "OPEN",
                "external_url": f"https://recruit.zoho.in/recruit/org{ATS_PORTAL_ID}/tab/JobOpenings/{job.get('id')}"
            })

        return {
            "statusCode": 200,
            "body": json.dumps(jobs)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


# POST /candidates

def create_candidate(event, context):
    try:
        data = json.loads(event["body"])

        # Validation
        for field in ["name", "email", "phone", "resume_url", "job_id"]:
            if field not in data:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"Missing field: {field}"})
                }

    
        # 1️⃣ Create Candidate in Zoho
        
        candidate_payload = {
            "data": [{
                "Last_Name": data["name"],
                "Email": data["email"],
                "Mobile": data["phone"],
                "Resume": data["resume_url"]
            }]
        }

        candidate_resp = requests.post(
            f"{ATS_BASE_URL}/recruit/v2/Candidates",
            headers=HEADERS,
            json=candidate_payload
        )

        if candidate_resp.status_code not in [200, 201]:
            return {
                "statusCode": candidate_resp.status_code,
                "body": json.dumps({"error": "Candidate creation failed"})
            }

        candidate_id = candidate_resp.json()["data"][0]["details"]["id"]

       
        # 2️⃣ Create Application (Attach Candidate to Job)
       
        application_payload = {
            "data": [{
                "Candidate_Name": candidate_id,
                "Job_Opening_Name": data["job_id"],
                "Application_Status": "Applied"
            }]
        }

        application_resp = requests.post(
            f"{ATS_BASE_URL}/recruit/v2/Applications",
            headers=HEADERS,
            json=application_payload
        )

        if application_resp.status_code not in [200, 201]:
            return {
                "statusCode": application_resp.status_code,
                "body": json.dumps({"error": "Application creation failed"})
            }

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Candidate created and assigned to job successfully",
                "candidate_id": candidate_id
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


# GET /applications

def get_applications(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        job_id = params.get("job_id")

        if not job_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "job_id is required"})
            }

        url = f"{ATS_BASE_URL}/recruit/v2/Applications"
        query = {
            "portal_id": ATS_PORTAL_ID,
            "fields": "Candidate_Name,Email,Application_Status",
            "page": params.get("page", 1),
            "per_page": params.get("limit", 10)
        }

        response = requests.get(url, headers=HEADERS, params=query)

        if response.status_code != 200:
            return {
                "statusCode": response.status_code,
                "body": json.dumps({"error": "Failed to fetch applications"})
            }

        applications = []
        for app in response.json().get("data", []):
            applications.append({
                "id": app.get("id"),
                "candidate_name": app.get("Candidate_Name", {}).get("name"),
                "email": app.get("Email"),
                "status": app.get("Application_Status", "APPLIED")
            })

        return {
            "statusCode": 200,
            "body": json.dumps(applications)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
``
