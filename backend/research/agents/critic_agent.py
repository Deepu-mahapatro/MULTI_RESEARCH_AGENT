# ---------------------------------------------------------
# CRITIC AGENT
# ---------------------------------------------------------
# The Critic Agent reviews the research report against
# the research information collected by the Search Agent.
#
# It checks:
#
# 1. Relevance
# 2. Evidence
# 3. Completeness
# 4. Unsupported claims
# 5. Clarity
#
# The Critic returns:
#
# {
#     "status": "PASS",
#     "feedback": "..."
# }
#
# We intentionally keep the Critic response short because
# this agent is used only for validation, not for writing
# the final report.
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
# The Critic does not need a large output.
#
# 300 tokens is enough for:
#
#     STATUS: PASS
#
#     FEEDBACK:
#     Short evaluation...
#
# Keeping the output small reduces unnecessary generation
# and can improve response time and token usage.
# ---------------------------------------------------------

llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    max_tokens=300,
    reasoning_effort="none"
)


# ---------------------------------------------------------
# CRITIC FUNCTION
# ---------------------------------------------------------

def run_critic_agent(report, research_information):
    """
    Review a research report against the research
    information used to create it.

    Returns:
        {
            "status": "PASS" or "NEEDS IMPROVEMENT",
            "feedback": "..."
        }
    """

    # -----------------------------------------------------
    # COMPACT CRITIC PROMPT
    # -----------------------------------------------------
    # The Critic still receives both:
    #
    #     research information
    #     generated report
    #
    # because it needs the evidence to verify the report.
    #
    # However, the instructions are intentionally concise.
    # -----------------------------------------------------

    prompt = f"""
You are a strict research report critic.

Compare the REPORT against the RESEARCH INFORMATION.

Check:
- relevance to the research
- factual support
- important missing information
- unsupported claims
- clarity

Use ONLY the provided research information.
Do not add new facts.

RESEARCH INFORMATION:
{research_information}

REPORT:
{report}

Return ONLY this format:

STATUS: PASS
FEEDBACK: Brief evaluation.

STATUS must be exactly:
PASS
or
NEEDS IMPROVEMENT

If the report is adequately supported and well written,
use PASS.

If important problems exist, use NEEDS IMPROVEMENT.
Keep FEEDBACK under 60 words.
"""

    # -----------------------------------------------------
    # CALL LLM
    # -----------------------------------------------------

    response = llm.invoke(prompt)

    critic_text = response.content.strip()


    # -----------------------------------------------------
    # EXTRACT STATUS
    # -----------------------------------------------------

    if "STATUS: NEEDS IMPROVEMENT" in critic_text:

        status = "NEEDS IMPROVEMENT"

    elif "STATUS: PASS" in critic_text:

        status = "PASS"

    else:

        # If the model does not follow the expected format,
        # treat the result as needing attention.
        status = "NEEDS IMPROVEMENT"


    # -----------------------------------------------------
    # EXTRACT FEEDBACK
    # -----------------------------------------------------

    if "FEEDBACK:" in critic_text:

        feedback = critic_text.split(
            "FEEDBACK:",
            1
        )[1].strip()

    else:

        feedback = critic_text


    # -----------------------------------------------------
    # RETURN STRUCTURED RESULT
    # -----------------------------------------------------

    return {
        "status": status,
        "feedback": feedback
    }