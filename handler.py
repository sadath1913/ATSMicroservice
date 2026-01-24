import json
import uuid
import os

DATA_FILE = "applications.json"

def read_applications():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_applications(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# In-memory storage (simulates ATS)
CANDIDATES = []
APPLICATIONS = []
def health_check(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "Serverless service is running"
        })
    }

def get_jobs(event, context):
    """
    Mocked jobs response.
    In real integration, this will call Breezy HR jobs API.
    """

    jobs = [
        {
            "id": "job_001",
            "title": "Backend Developer",
            "location": "Bangalore",
            "status": "OPEN",
            "external_url": "https://careers.example.com/job_001"
        },
        {
            "id": "job_002",
            "title": "Frontend Intern",
            "location": "Remote",
            "status": "OPEN",
            "external_url": "https://careers.example.com/job_002"
        }
    ]

    return {
        "statusCode": 200,
        "body": json.dumps(jobs)
    }
def create_candidate(event, context):
    try:
        # 🔹 ERROR HANDLING: body missing
        if "body" not in event or event["body"] is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Request body is missing"})
            }

        # 🔹 ERROR HANDLING: invalid JSON
        try:
            data = json.loads(event["body"])
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid JSON format"})
            }

        # 🔹 REQUIRED FIELDS CHECK
        for field in ["name", "email", "job_id"]:
            if field not in data:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"Missing field: {field}"})
                }

        # 🔹 CREATE APPLICATION (assignment)
        application = {
            "id": str(uuid.uuid4()),
            "candidate_name": data["name"],
            "email": data["email"],
            "job_id": data["job_id"],
            "status": "APPLIED"
        }

        applications = read_applications()
        applications.append(application)
        write_applications(applications)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Candidate created and assigned to job",
                "application": application
            })
        }

    except Exception:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to create candidate"})
        }

        
def get_applications(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        job_id = params.get("job_id")

        if not job_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "job_id is required"})
            }

        applications = read_applications()
        filtered = [a for a in applications if a["job_id"] == job_id]

        # 🔹 PAGINATION
        page = int(params.get("page", 1))
        limit = int(params.get("limit", 10))

        start = (page - 1) * limit
        end = start + limit

        paginated = filtered[start:end]

        return {
            "statusCode": 200,
            "body": json.dumps({
                "page": page,
                "limit": limit,
                "total": len(filtered),
                "data": paginated
            })
        }


    except Exception:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to fetch applications"})
        }
