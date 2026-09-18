# ---------------------------------------------------------
# WRITER AGENT
# ---------------------------------------------------------
# The Writer Agent converts collected research information
# into a structured research report.
#
# It supports:
#
# 1. Creating a first report.
# 2. Revising a report using Critic feedback.
# ---------------------------------------------------------


from langchain_groq import ChatGroq
from dotenv import load_dotenv


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# GROQ LLM
# ---------------------------------------------------------
# The Writer needs enough output space to complete all
# required sections.
#
# We keep the output concise because the current Groq
# organization has a limited token budget.
# ---------------------------------------------------------

llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    max_tokens=1000,
    reasoning_effort="none"
)


# ---------------------------------------------------------
# WRITER FUNCTION
# ---------------------------------------------------------

def run_writer_agent(
    research_information,
    previous_report=None,
    critic_feedback=None
):
    """
    Generate a new research report or improve an existing
    report using Critic Agent feedback.

    Parameters:
        research_information:
            Information collected by the Search Agent.

        previous_report:
            Previous generated report.
            None when creating the first report.

        critic_feedback:
            Feedback from the Critic Agent.
            None when creating the first report.

    Returns:
        The generated research report.
    """


    # -----------------------------------------------------
    # FIRST REPORT
    # -----------------------------------------------------

    if previous_report is None:

        prompt = f"""
You are a professional research report writer.

Create a COMPLETE and CONCISE research report using ONLY
the research information provided below.

RESEARCH INFORMATION:
{research_information}

==================================================
REQUIRED REPORT FORMAT
==================================================

# Research Report

## 1. Introduction
Write 2-3 concise sentences introducing the topic.

## 2. Main Findings
Provide 3-4 important findings.
Use bullet points.
Each finding should be 1-2 concise sentences.

## 3. Benefits
Provide 2-3 important benefits.
Use bullet points.
Each benefit should be 1-2 concise sentences.

## 4. Challenges
Provide 2-3 important challenges.
Use bullet points.
Each challenge should be 1-2 concise sentences.

## 5. Conclusion
Write 2-3 concise sentences summarizing the research.

==================================================
STRICT RULES
==================================================

- ALL FIVE sections are mandatory.
- The report MUST end with "## 5. Conclusion".
- Never stop before the Conclusion.
- Keep every section concise.
- Do not write a long introduction.
- Do not repeat the same information.
- Use only information supported by the research.
- Do not invent facts.
- Do not add unsupported claims.
- Use Markdown headings exactly as shown above.
- Use "-" for bullet points.
- Return ONLY the report.
"""


    # -----------------------------------------------------
    # IMPROVE EXISTING REPORT
    # -----------------------------------------------------

    else:

        prompt = f"""
You are a professional research report writer.

Improve the previous research report using the Critic
Agent's feedback.

Use ONLY the provided research information.

==================================================
RESEARCH INFORMATION
==================================================

{research_information}

==================================================
PREVIOUS REPORT
==================================================

{previous_report}

==================================================
CRITIC FEEDBACK
==================================================

{critic_feedback}

==================================================
REQUIRED REPORT FORMAT
==================================================

# Research Report

## 1. Introduction
Write 2-3 concise sentences.

## 2. Main Findings
Provide 3-4 important findings.
Use bullet points.

## 3. Benefits
Provide 2-3 important benefits.
Use bullet points.

## 4. Challenges
Provide 2-3 important challenges.
Use bullet points.

## 5. Conclusion
Write 2-3 concise sentences.

==================================================
STRICT RULES
==================================================

- ALL FIVE sections are mandatory.
- The report MUST end with "## 5. Conclusion".
- Never stop before the Conclusion.
- Fix the specific problems identified by the Critic.
- Keep every section concise.
- Do not repeat information unnecessarily.
- Use only information supported by the research.
- Do not invent facts.
- Do not introduce unsupported claims.
- Use Markdown headings exactly as shown above.
- Use "-" for bullet points.
- Return ONLY the improved report.
- Do not explain your changes.
"""


    # -----------------------------------------------------
    # SEND REQUEST TO GROQ
    # -----------------------------------------------------

    response = llm.invoke(prompt)


    # -----------------------------------------------------
    # GET GENERATED REPORT
    # -----------------------------------------------------

    report = response.content.strip()


    # -----------------------------------------------------
    # RETURN REPORT
    # -----------------------------------------------------

    return report