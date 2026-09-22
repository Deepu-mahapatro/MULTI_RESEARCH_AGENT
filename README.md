# 🤖 Multi-Agent AI Research Assistant

<p align="center">

  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">

  <img src="https://img.shields.io/badge/Django-6.x-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">

  <img src="https://img.shields.io/badge/REST%20API-Django%20REST%20Framework-red?style=for-the-badge" alt="DRF">

  <img src="https://img.shields.io/badge/AI-LangChain-1C3C3C?style=for-the-badge" alt="LangChain">

  <img src="https://img.shields.io/badge/LLM-Groq-orange?style=for-the-badge" alt="Groq">

  <img src="https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">

  <img src="https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black" alt="Render">

</p>

<p align="center">

  <strong>🔍 Search • 📖 Analyze • ✍️ Write • 🧐 Review • 📝 Summarize</strong>

</p>

<p align="center">

  <a href="https://frontend-research-agent.onrender.com">
    <img src="https://img.shields.io/badge/🚀%20Live%20Demo-Open%20ResearchAI-success?style=for-the-badge" alt="Live Demo">
  </a>

</p>

---

## 📌 Overview

**Multi-Agent AI Research Assistant** is a full-stack AI-powered research application that automates the process of researching a topic and generating a structured research report.

Instead of manually searching multiple websites, reading sources, collecting information, writing a report, and reviewing the result, the system performs these tasks through a multi-stage AI workflow.

The application combines:

- 🔍 Web search
- 🌐 Web scraping
- 🤖 Large Language Models
- 🧠 Multi-agent workflow
- 🧐 AI-based report review
- 📝 Automatic summarization
- 📄 PDF report generation
- 🗄️ PostgreSQL database storage
- ⚡ Background research processing

---

# ✨ Features

### 🔍 Intelligent Web Search

Uses **Tavily** to search the web and identify relevant sources for the research topic.

The system collects:

- Source titles
- Source URLs
- Search snippets
- Relevant webpage content

---

### 🌐 Web Scraping

Selected sources are processed using:

- `Requests`
- `BeautifulSoup`

The scraper:

- Downloads webpage content
- Removes unnecessary HTML elements
- Extracts readable text
- Detects common blocked/error pages
- Limits extracted content to a manageable size

---

### 🤖 Multi-Agent Research Workflow

The research process is divided into specialized stages:

```text
User
  │
  ▼
Django REST API
  │
  ▼
🔍 Search Agent
  │
  ▼
🌐 Web Scraper
  │
  ▼
✍️ Writer Agent
  │
  ▼
🧐 Critic Agent
  │
  ├── ✅ PASS
  │      │
  │      ▼
  │   📝 Summary Agent
  │
  └── ⚠️ NEEDS IMPROVEMENT
           │
           ▼
       ✍️ Writer Revision
           │
           ▼
       🧐 Final Critic
           │
           ▼
       📝 Summary Agent
           │
           ▼
      📄 Final Report

⚡ Background Processing

Research requests are processed in the background so that the API can immediately return a research ID while the AI workflow continues.

The frontend uses the research ID to monitor the progress of the task.

📊 Research Progress Tracking

The system tracks the research process through:

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

📄 PDF Report Generation

Completed research reports can be converted into downloadable PDF documents using ReportLab.

📚 Source Management

Research sources are stored in PostgreSQL together with the research request.

Each source can contain:

Title
URL
Search snippet
Creation timestamp

🧠 AI Agents
1. 🔍 Search Agent

The Search Agent is responsible for finding relevant information from the web.

Responsibilities
Search using Tavily
Collect relevant URLs
Extract source titles
Prepare source information
Scrape selected sources
Process multiple URLs concurrently

2. ✍️ Writer Agent

The Writer Agent generates the main research report using the collected research information.

The report follows a structured format:

# Research Report

## 1. Introduction

## 2. Main Findings

## 3. Benefits

## 4. Challenges

## 5. Conclusion

The Writer Agent is instructed to:

Use the provided research information
Avoid unsupported claims
Maintain a professional structure
Produce a clear research report

3. 🧐 Critic Agent

The Critic Agent reviews the generated report against the collected research information.

It checks:

Relevance
Factual support
Missing information
Unsupported claims
Clarity

The critic returns one of two statuses:

STATUS: PASS

or:

STATUS: NEEDS IMPROVEMENT

If improvement is required, the report is sent back to the Writer Agent for revision.

4. 📝 Summary Agent

After the final report is approved, the Summary Agent generates a concise summary of the report.

The summary:

Uses only information from the final report
Focuses on important findings
Avoids introducing new information
Uses clear professional language

🏗️ System Architecture
                         ┌─────────────────────┐
                         │        USER         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  HTML / CSS / JS    │
                         │      Frontend       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Django REST API  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Search Agent     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Tavily Search     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Web Scraper     │
                         │ Requests + BS4      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Writer Agent     │
                         │   Groq + Qwen LLM   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Critic Agent     │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
                  ✅ PASS                  ⚠️ NEEDS IMPROVEMENT
                     │                             │
                     │                             ▼
                     │                      Writer Revision
                     │                             │
                     │                             ▼
                     │                       Final Critic
                     │                             │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Summary Agent     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Final Research    │
                         │       Report        │
                         └──────────┬──────────┘
                                    │
                          ┌─────────┴─────────┐
                          ▼                   ▼
                    📄 Report Page       📥 PDF Export

🔄 Research Workflow

The complete research lifecycle is:

1️⃣ User submits a research question
            ↓
2️⃣ Django creates a research record
            ↓
3️⃣ Search Agent searches the web
            ↓
4️⃣ Relevant sources are collected
            ↓
5️⃣ Selected webpages are scraped
            ↓
6️⃣ Research information is prepared
            ↓
7️⃣ Writer Agent generates the report
            ↓
8️⃣ Critic Agent reviews the report
            ↓
9️⃣ If needed → Writer revises the report
            ↓
🔟 Final Critic review
            ↓
1️⃣1️⃣ Summary Agent creates a concise summary
            ↓
1️⃣2️⃣ Final report is stored
            ↓
1️⃣3️⃣ User can view and download the report

🛠️ Tech Stack

🎨 Frontend
HTML5
CSS3
JavaScript

⚙️ Backend
Python 3.12
Django
Django REST Framework

🤖 AI / LLM
LangChain
Groq
Qwen

🔎 Search
Tavily

🌐 Web Scraping
Requests
BeautifulSoup

🗄️ Database
PostgreSQL
Supabase

📄 PDF Generation
ReportLab

🚀 Deployment
Render

📁 Project Structure
MULTI_RESEARCH_AGENT/
│
├── 📄 README.md
├── 📄 LICENSE
├── 📄 .gitignore
│
├── 📂 backend/
│   │
│   ├── 🔐 .env.example
│   ├── 📄 requirements.txt
│   ├── 📄 manage.py
│   │
│   ├── 📂 config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── ...
│   │
│   └── 📂 research/
│       │
│       ├── 📂 agents/
│       │   ├── search_agent.py
│       │   ├── writer_agent.py
│       │   ├── critic_agent.py
│       │   └── summary_agent.py
│       │
│       ├── 📂 migrations/
│       │
│       ├── models.py
│       ├── serializers.py
│       ├── services.py
│       ├── tools.py
│       ├── views.py
│       ├── urls.py
│       └── pdf_service.py
│
├── 📂 frontend/
│   │
│   ├── index.html
│   │
│   ├── 📂 pages/
│   │   ├── research.html
│   │   ├── progress.html
│   │   └── report.html
│   │
│   ├── 📂 css/
│   │   ├── style.css
│   │   ├── research.css
│   │   ├── progress.css
│   │   └── report.css
│   │
│   └── 📂 js/
│       ├── app.js
│       ├── research.js
│       ├── progress.js
│       └── report.js
│
└── 📂 docs/
    ├── architecture.md
    ├── workflow.md
    ├── api.md
    │
    └── 📂 screenshots/
        ├── research.png
        ├── progress.png
        ├── report.png
        └── pdf.png

⚙️ Installation & Setup

1️⃣ Clone the Repository
git clone https://github.com/Deepu-mahapatro/MULTI_RESEARCH_AGENT.git

Move into the project:

cd MULTI_RESEARCH_AGENT

2️⃣ Backend Setup

Move into the backend directory:

cd backend

Create a virtual environment:

python -m venv venv
Windows

Activate the virtual environment:

venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt

3️⃣ Environment Variables

Create a .env file inside the backend directory:

backend/.env

Add:

SECRET_KEY=your_django_secret_key
DEBUG=False

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=5432

TAVILY_API_KEY=your_tavily_api_key

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=qwen/qwen3.8-27b

⚠️ Never commit your .env file to GitHub.

4️⃣ Database Setup

Run Django migrations:

python manage.py makemigrations
python manage.py migrate

5️⃣ Run the Backend

Start the Django development server:

python manage.py runserver

The backend will run at:

http://127.0.0.1:8000

6️⃣ Run the Frontend

Open the frontend directory using a local development server such as VS Code Live Server.

The frontend communicates with the Django REST API.

🔌 API Endpoints
Method	Endpoint	Description
GET	/api/test/	Check API availability
GET	/api/research/	Retrieve research records
POST	/api/research/	Start a new research task
GET	/api/research/<id>/	Retrieve a specific research
PUT	/api/research/<id>/	Update a research
DELETE	/api/research/<id>/	Delete a research
GET	/api/research/<id>/pdf/	Download completed report as PDF

📤 Create Research
Request
POST /api/research/
Body
{
    "question": "Impact of artificial intelligence on healthcare"
}
Response

The API returns a research ID and the initial research information.

The research workflow then continues in the background.

📥 PDF Report

🌐 Live Demo
🚀 ResearchAI

Try the deployed application:

👉 Open ResearchAI
https://frontend-research-agent.onrender.com

🚀 Deployment
The application is deployed using the following architecture:

┌───────────────────────────────┐
│       Render Static Site      │
│           Frontend            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Render Web Service      │
│      Django REST Backend      │
└───────────────┬───────────────┘
                │
        ┌───────┼────────┐
        ▼       ▼        ▼
     Tavily    Groq    Supabase
     Search     LLM    PostgreSQL

Production Services
Component	Platform
Frontend	Render Static Site
Backend	Render Web Service
Database	Supabase PostgreSQL
Web Search	Tavily
LLM	Groq
PDF Generation	ReportLab

🔐 Security Notes

Sensitive configuration values are stored using environment variables.

The following values must never be committed to GitHub:

.env
GROQ_API_KEY
TAVILY_API_KEY
DB_PASSWORD
SECRET_KEY

Use:

backend/.env.example

to document the required environment variables without exposing real credentials.

Recommended GitHub protection
.env              ❌ Never commit
.env.example      ✅ Safe template
venv/             ❌ Never commit
__pycache__/      ❌ Never commit

🔮 Future Improvements

Possible future improvements include:

⚡ More advanced background task processing
🔎 Improved source ranking and filtering
📚 More advanced research synthesis
🤖 Additional specialized research agents
🌐 Better handling of dynamically rendered webpages
🚀 Further production performance optimization
📊 More advanced research insights
📄 License

This project is licensed under the MIT License.
