# 🔄 Research Workflow

## 📌 Overview

The **Multi-Agent AI Research Agent** follows a sequential workflow to collect information, generate a research report, review it, and produce a final summary.

```text
User
 ↓
Frontend
 ↓
Django REST API
 ↓
Search Agent
 ↓
Web Scraping
 ↓
Writer Agent
 ↓
Critic Agent
 ↓
Revision if Required
 ↓
Summary Agent
 ↓
Final Report
1. 📝 Research Request

The user enters a research question through the frontend.

The frontend sends the question to the Django REST API:

POST /api/research/

The backend creates a research record and returns a unique research ID.

2. 🔍 Search Stage

The Search Agent receives the research question.

It uses Tavily to search the web and collect relevant sources.

Research Question
       ↓
Tavily Search
       ↓
Search Results
       ↓
Source URLs

The selected source information is stored in the database.

3. 🌐 Reading & Scraping Stage

The system selects sources from the search results and scrapes their content using:

Requests
BeautifulSoup
Source URL
    ↓
HTTP Request
    ↓
HTML Content
    ↓
BeautifulSoup
    ↓
Clean Text

The extracted information becomes the research context for the AI agents.

4. ✍️ Writing Stage

The Writer Agent uses the collected research information to generate the initial report.

The current implementation uses:

Groq
  ↓
Qwen Model

The report follows a structured format containing:

Introduction
Main Findings
Benefits
Challenges
Conclusion
5. 🧐 Review Stage

The Critic Agent evaluates the generated report against the research information.

It checks:

Relevance
Factual support
Missing information
Unsupported claims
Clarity

The result is either:

PASS

or:

NEEDS IMPROVEMENT
6. 🔄 Revision Stage

If the Critic Agent returns NEEDS IMPROVEMENT, the report is sent back to the Writer Agent for revision.

Writer
  ↓
Critic
  ↓
NEEDS IMPROVEMENT
  ↓
Writer Revision
  ↓
Final Critic

If the report passes review, the workflow continues directly to the summary stage.

7. 📝 Summary Stage

The Summary Agent generates a concise summary from the final research report.

It only uses information already present in the report and does not add new facts.

Final Report
     ↓
Summary Agent
     ↓
Concise Summary
8. 💾 Database Storage

The final research information is stored in PostgreSQL.

The system stores:

Research question
Research status
Final report
Summary
Critic status
Critic feedback
Research sources
Timestamps

The production database is hosted using Supabase PostgreSQL.

9. 📊 Progress Tracking

The research status is updated throughout the workflow.

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

The frontend uses these statuses to display the current research progress.

10. 📄 Final Report

Once the workflow is completed, the frontend retrieves the final research data using:

GET /api/research/<id>/

The user can then:

Read the research report
View the summary
View research sources
Download the report as PDF

PDF generation is handled by ReportLab.

🏁 Complete Workflow
User enters question
        ↓
Frontend
        ↓
Django REST API
        ↓
Create Research Record
        ↓
Search Agent
        ↓
Tavily Web Search
        ↓
Web Scraping
        ↓
Research Information
        ↓
Writer Agent
        ↓
Generated Report
        ↓
Critic Agent
        ↓
   ┌────┴────┐
   ↓         ↓
 PASS   NEEDS IMPROVEMENT
   ↓         ↓
   │    Writer Revision
   │         ↓
   │    Final Critic
   └────┬────┘
        ↓
Summary Agent
        ↓
Final Report + Summary
        ↓
PostgreSQL
        ↓
Frontend
        ↓
PDF Download
