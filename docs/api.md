# 🔌 API Documentation

## 📌 Overview

The **Multi-Agent AI Research Agent** provides a REST API built with **Django REST Framework**.

The API handles research creation, progress tracking, report retrieval, record management, and PDF generation.

## 🌐 Base URL

```text
https://multi-research-agent-luez.onrender.com/api/
📋 Endpoints
Method	Endpoint	Description
GET	/test/	Check API status
GET	/research/	Get all research records
POST	/research/	Start a new research
GET	/research/<id>/	Get a specific research
PUT	/research/<id>/	Update a research
DELETE	/research/<id>/	Delete a research
GET	/research/<id>/pdf/	Download research as PDF
🧪 Test API
Request
GET /api/test/
Response
{
    "message": "ResearchAI API is working!"
}
🚀 Create Research
Request
POST /api/research/
Content-Type: application/json
Body
{
    "question": "What are the applications of AI in healthcare?"
}
Response
{
    "message": "Research started.",
    "research": {
        "id": 15,
        "question": "What are the applications of AI in healthcare?",
        "status": "pending",
        "final_report": "",
        "summary": "",
        "critic_status": "",
        "critic_feedback": "",
        "sources": [],
        "created_at": "2026-09-22T10:00:00Z",
        "updated_at": "2026-09-22T10:00:00Z"
    }
}

Status: 201 Created

The research workflow continues in the background after the research ID is returned.

🔎 Get Research
Request
GET /api/research/<id>/
Example
GET /api/research/15/

Returns the current status, generated report, summary, critic feedback, and sources.

📊 Research Status

The research workflow uses the following statuses:

pending
   ↓
searching
   ↓
reading
   ↓
writing
   ↓
reviewing
   ↓
completed

If an error occurs:

failed

The frontend uses these statuses to display the research progress.

📄 Download PDF
Request
GET /api/research/<id>/pdf/

Example:

GET /api/research/15/pdf/

The endpoint generates a PDF of the completed research report using ReportLab.

A report must have:

status = completed

before it can be downloaded.

✏️ Update Research
Request
PUT /api/research/<id>/

Example:

{
    "question": "What are the latest applications of AI in healthcare?"
}

The backend-managed fields such as status, final_report, summary, and critic_feedback are read-only.

🗑️ Delete Research
Request
DELETE /api/research/<id>/

Example:

DELETE /api/research/15/

Status: 204 No Content

Deleting a research also removes its associated sources.

❌ Common Response Codes
Code	Meaning
200	Request successful
201	Research created
204	Research deleted
400	Invalid request
404	Research not found
🔄 API Workflow
User
  ↓
POST /research/
  ↓
Research ID
  ↓
GET /research/<id>/
  ↓
Track Status
  ↓
Completed
  ↓
View Report
  ↓
GET /research/<id>/pdf/

The API provides a simple interface between the frontend and the backend research workflow.
