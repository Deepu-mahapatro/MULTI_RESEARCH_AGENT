# 🏗️ System Architecture

## 📌 Overview

The **Multi-Agent AI Research Agent** is a full-stack AI research application that combines a JavaScript frontend, Django REST API, specialized AI agents, web search, web scraping, PostgreSQL, and PDF generation.

The system follows a sequential research workflow where each stage performs a specific responsibility.

---

# 🧩 High-Level Architecture

```text
┌─────────────────────────────────────┐
│              USER                   │
│                                     │
│     Enters a research question     │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│          FRONTEND                   │
│                                     │
│      HTML + CSS + JavaScript        │
│                                     │
│  • Research Interface               │
│  • Progress Tracking                │
│  • Report Display                   │
└──────────────────┬──────────────────┘
                   │
                   │ HTTP / REST API
                   ▼
┌─────────────────────────────────────┐
│        DJANGO REST API              │
│                                     │
│  • Research Creation                │
│  • Research Status                  │
│  • Research Retrieval               │
│  • PDF Download                     │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│       RESEARCH SERVICE              │
│                                     │
│  Coordinates the complete workflow  │
└──────────────────┬──────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │    SEARCH AGENT      │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   TAVILY WEB SEARCH  │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │    WEB SCRAPER       │
        │ Requests +           │
        │ BeautifulSoup        │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │    WRITER AGENT      │
        │                      │
        │    Groq + Qwen       │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │    CRITIC AGENT      │
        └──────────┬───────────┘
                   │
            ┌──────┴──────┐
            │             │
            ▼             ▼
         PASS       NEEDS IMPROVEMENT
            │             │
            │             ▼
            │      ┌───────────────┐
            │      │ Writer Agent  │
            │      │   Revision    │
            │      └───────┬───────┘
            │              │
            │              ▼
            │       ┌──────────────┐
            │       │ Final Critic │
            │       └──────┬───────┘
            │              │
            └──────┬───────┘
                   │
                   ▼
        ┌──────────────────────┐
        │    SUMMARY AGENT     │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │    FINAL REPORT      │
        └──────────┬───────────┘
                   │
          ┌────────┴────────┐
          ▼                 ▼
┌─────────────────┐  ┌─────────────────┐
│ PostgreSQL /    │  │ PDF Generation  │
│ Supabase        │  │   ReportLab     │
└─────────────────┘  └─────────────────┘
🎨 1. Frontend Layer

The frontend provides the user interface for interacting with the research system.

Technologies
HTML5
CSS3
JavaScript
Main Pages
frontend/
│
├── index.html
│
└── pages/
    ├── research.html
    ├── progress.html
    └── report.html
Responsibilities

The frontend is responsible for:

Accepting the user's research question
Sending research requests to the backend
Receiving the research ID
Tracking research progress
Displaying the final report
Displaying research sources
Providing PDF download functionality

The frontend communicates with the Django backend using HTTP requests.

⚙️ 2. Backend Layer

The backend is built using:

Python
Django
Django REST Framework

The backend acts as the central coordinator between the frontend, AI workflow, external services, and database.

Main Backend Components
backend/
│
├── config/
│
└── research/
    ├── agents/
    ├── models.py
    ├── serializers.py
    ├── services.py
    ├── tools.py
    ├── views.py
    ├── urls.py
    └── pdf_service.py
🔌 3. Django REST API

The Django REST API provides endpoints used by the frontend.

Main Responsibilities
Create research tasks
Retrieve research information
Update research records
Delete research records
Track research status
Provide completed reports
Generate PDF downloads

The API creates the research record first and then starts the research workflow in the background.

🧠 4. Research Service Layer

The research service coordinates the complete AI workflow.

The main workflow is handled by:

process_research()

The service controls the sequence:

Search
  ↓
Read / Prepare Research
  ↓
Write
  ↓
Review
  ↓
Revision if Required
  ↓
Summary
  ↓
Completed

The service also updates the research status in PostgreSQL during each stage.

🔍 5. Search Agent

The Search Agent is responsible for gathering information from the web.

Process
Research Question
       ↓
Tavily Search
       ↓
Search Results
       ↓
Extract URLs
       ↓
Select Sources
       ↓
Concurrent Scraping
       ↓
Research Information

The Search Agent uses:

Tavily
Requests
BeautifulSoup
Python concurrency

The system searches for multiple sources and concurrently scrapes selected URLs to reduce unnecessary sequential waiting.

🌐 6. Web Scraping Layer

The web scraping functionality is implemented using:

Requests
BeautifulSoup

The scraper:

Downloads the webpage
Checks the HTTP response
Parses the HTML
Removes unnecessary elements
Extracts readable text
Detects common blocked/error pages
Limits the returned content

The extracted information is then passed to the research workflow.

✍️ 7. Writer Agent

The Writer Agent uses the collected research information to generate the main report.

The current production implementation uses:

Groq
  ↓
Qwen Model

The Writer Agent generates a structured report containing:

Research Report
│
├── Introduction
├── Main Findings
├── Benefits
├── Challenges
└── Conclusion

The Writer Agent is instructed to rely on the provided research information and avoid unsupported claims.

🧐 8. Critic Agent

The Critic Agent evaluates the generated report against the collected research information.

Review Criteria
Relevance
Factual support
Missing information
Unsupported claims
Clarity

The Critic Agent returns:

STATUS: PASS

or:

STATUS: NEEDS IMPROVEMENT
🔄 9. Revision Loop

If the Critic Agent identifies important problems, the report enters a revision cycle.

Writer
  ↓
Critic
  ↓
NEEDS IMPROVEMENT
  ↓
Writer Revision
  ↓
Final Critic
  ↓
Summary

If the report passes review:

Writer
  ↓
Critic
  ↓
PASS
  ↓
Summary

This allows the system to perform an additional quality-checking stage before producing the final result.

📝 10. Summary Agent

After the final report is produced, the Summary Agent creates a concise summary.

The Summary Agent:

Uses only information from the final report
Focuses on important findings
Avoids adding new facts
Produces a concise professional summary

The final summary is stored with the research record.

🗄️ 11. Database Layer

The application uses PostgreSQL for persistent storage.

The production database is hosted using Supabase PostgreSQL.

Main Models

The system stores research information using:

Research
ResearchSource
Research

Stores:

Research question
Current status
Final report
Summary
Critic status
Critic feedback
Creation timestamp
Update timestamp
ResearchSource

Stores:

Research reference
Source title
Source URL
Source snippet
Creation timestamp
📄 12. PDF Generation

Completed research reports can be converted into PDF documents.

The PDF functionality is implemented using:

ReportLab

The process is:

Completed Research
       ↓
Final Report
       ↓
PDF Service
       ↓
ReportLab
       ↓
PDF Response
       ↓
User Download

The backend only allows the PDF to be generated when the research status is:

completed
⚡ 13. Background Processing

Research processing runs in a background thread after the research request is created.

The basic flow is:

POST /api/research/
        │
        ▼
Create Research Record
        │
        ▼
Start Background Thread
        │
        ▼
Return Research ID
        │
        └───────────────┐
                        ▼
                 Research Workflow

This allows the API to respond without waiting for the entire research workflow to finish.

📊 14. Research Status System

The backend maintains the following research states:

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

Any Stage
   ↓
failed

The frontend uses these states to display the current research progress to the user.

🔐 15. Environment & Configuration

Sensitive configuration values are loaded through environment variables.

Examples include:

SECRET_KEY
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
TAVILY_API_KEY
GROQ_API_KEY
GROQ_MODEL

The actual .env file is not committed to the repository.

A .env.example file is provided as a configuration template.

🚀 16. Production Architecture

The deployed application uses:

┌──────────────────────────────────────┐
│            User Browser              │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│       Render Static Site             │
│             Frontend                 │
└──────────────────┬───────────────────┘
                   │
                   │ REST API
                   ▼
┌──────────────────────────────────────┐
│       Render Web Service             │
│        Django Backend                │
└───────────────┬───────┬──────────────┘
                │       │
        ┌───────┘       └────────┐
        ▼                        ▼
┌───────────────┐       ┌────────────────┐
│ Tavily Search │       │ Groq + Qwen    │
└───────────────┘       └────────────────┘
                │
                ▼
       ┌─────────────────┐
       │ Supabase        │
       │ PostgreSQL      │
       └─────────────────┘
Production Services
Component	Service
Frontend	Render Static Site
Backend	Render Web Service
Database	Supabase PostgreSQL
Web Search	Tavily
LLM	Groq + Qwen
PDF Generation	ReportLab
🔗 17. Component Communication

The major communication flow is:

Frontend
   │
   │ HTTP
   ▼
Django REST API
   │
   ▼
Research Service
   │
   ├──────► Search Agent
   │             │
   │             ▼
   │          Tavily
   │             │
   │             ▼
   │         Web Scraper
   │
   ├──────► Writer Agent
   │             │
   │             ▼
   │        Groq + Qwen
   │
   ├──────► Critic Agent
   │
   └──────► Summary Agent
   │
   ▼
PostgreSQL
🏁 Architecture Summary

The application follows a modular architecture where each major component has a focused responsibility.

Frontend
   ↓
Django REST API
   ↓
Research Service
   ↓
Search + Scraping
   ↓
Writer
   ↓
Critic
   ↓
Revision if Required
   ↓
Summary
   ↓
PostgreSQL
   ↓
PDF Export

This separation makes the system easier to understand, maintain, and extend with additional research capabilities in the future.
