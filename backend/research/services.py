# ---------------------------------------------------------
# RESEARCH SERVICES
# ---------------------------------------------------------
# This file coordinates the complete ResearchAI workflow.
#
# Workflow:
#
# User Question
#       ↓
# Search Agent
#       ↓
# Save Sources
#       ↓
# Research Information
#       ↓
# Writer Agent
#       ↓
# Draft Report
#       ↓
# Critic Agent
#       ↓
# PASS ───────────────→ Final Report
#
# OR
#
# NEEDS IMPROVEMENT
#       ↓
# Writer Agent
#       ↓
# Improved Report
#       ↓
# Critic Agent
#
# The Research model status is updated after each major
# stage so the Progress Page can display the current stage.
#
# For now, we allow only ONE revision attempt.
# ---------------------------------------------------------


# ---------------------------------------------------------
# IMPORT AGENTS
# ---------------------------------------------------------

from research.agents.search_agent import run_search_agent
from research.agents.writer_agent import run_writer_agent
from research.agents.critic_agent import run_critic_agent
from research.agents.summary_agent import run_summary_agent


# ---------------------------------------------------------
# IMPORT MODELS
# ---------------------------------------------------------

from research.models import ResearchSource


# ---------------------------------------------------------
# MAIN RESEARCH WORKFLOW
# ---------------------------------------------------------

def process_research(research):
    """
    Run the complete ResearchAI workflow.

    Parameters:
        research:
            A Research model object containing the user's
            research question and current status.

    Workflow:

        1. Search Agent
        2. Save research sources
        3. Read / scrape information
        4. Writer Agent
        5. Critic Agent
        6. Optional Writer revision
        7. Final Critic review
        8. Generate summary
        9. Save final result
        10. Mark research as completed
    """

    # -----------------------------------------------------
    # STEP 1: SEARCH AGENT
    # -----------------------------------------------------

    research.status = "searching"

    research.save(
        update_fields=["status", "updated_at"]
    )

    print("STEP 1: Starting Search Agent")

    search_result = run_search_agent(
        research.question
    )

    print("STEP 1: Search Agent completed")


    # -----------------------------------------------------
    # STEP 1.5: SAVE SOURCES
    # -----------------------------------------------------

    print("STEP 1.5: Saving research sources")

    # Remove existing sources for this research.
    #
    # This prevents duplicate sources if the same research
    # workflow is ever processed again.
    ResearchSource.objects.filter(
        research=research
    ).delete()

    # Create one ResearchSource record for every source
    # returned by the Search Agent.
    for source in search_result["sources"]:

        ResearchSource.objects.create(
            research=research,
            title=source["title"],
            url=source["url"],
            snippet=source.get("snippet", "")
        )

    print(
        "STEP 1.5: Saved "
        f"{len(search_result['sources'])} sources"
    )


    # -----------------------------------------------------
    # STEP 2: READING / SCRAPING
    # -----------------------------------------------------

    research.status = "reading"

    research.save(
        update_fields=["status", "updated_at"]
    )

    print(
        "STEP 2: Preparing research information"
    )

    research_information = ""

    for item in search_result["scraped_results"]:

        research_information += (
            f"\n\nSOURCE URL: {item['url']}\n"
            f"CONTENT:\n{item['content']}"
        )

    print(
        "STEP 2: Research information prepared"
    )


    # -----------------------------------------------------
    # STEP 3: WRITER AGENT
    # -----------------------------------------------------

    research.status = "writing"

    research.save(
        update_fields=["status", "updated_at"]
    )

    print(
        "STEP 3: Starting Writer Agent"
    )

    final_report = run_writer_agent(
        research_information
    )

    print(
        "STEP 3: Writer Agent completed"
    )


    # -----------------------------------------------------
    # STEP 4: CRITIC AGENT
    # -----------------------------------------------------

    research.status = "reviewing"

    research.save(
        update_fields=["status", "updated_at"]
    )

    print(
        "STEP 4: Starting Critic Agent"
    )

    critic_result = run_critic_agent(
        final_report,
        research_information
    )

    print(
        "STEP 4: Critic Agent completed"
    )


    # -----------------------------------------------------
    # STEP 5: OPTIONAL REVISION
    # -----------------------------------------------------

    if critic_result["status"] == "NEEDS IMPROVEMENT":

        print(
            "STEP 5: Critic requested improvement"
        )


        # -------------------------------------------------
        # STEP 5A: WRITER REVISION
        # -------------------------------------------------

        research.status = "writing"

        research.save(
            update_fields=["status", "updated_at"]
        )

        print(
            "STEP 5: Starting Writer Revision"
        )

        final_report = run_writer_agent(
            research_information,
            previous_report=final_report,
            critic_feedback=critic_result["feedback"]
        )

        print(
            "STEP 5: Writer Revision completed"
        )


        # -------------------------------------------------
        # STEP 5B: FINAL CRITIC REVIEW
        # -------------------------------------------------

        research.status = "reviewing"

        research.save(
            update_fields=["status", "updated_at"]
        )

        print(
            "STEP 5: Starting Final Critic Review"
        )

        critic_result = run_critic_agent(
            final_report,
            research_information
        )

        print(
            "STEP 5: Final Critic Review completed"
        )

    else:

        print(
            "STEP 5: Critic approved the report"
        )


    # -----------------------------------------------------
    # STEP 6: GENERATE SUMMARY
    # -----------------------------------------------------
    #
    # Generate the summary only after the final report has
    # passed through the Critic Agent and any required
    # revision.
    # -----------------------------------------------------

    print(
        "STEP 6: Starting Summary Agent"
    )

    summary = run_summary_agent(
        final_report
    )

    print(
        "STEP 6: Summary Agent completed"
    )


    # -----------------------------------------------------
    # STEP 7: SAVE FINAL RESULT
    # -----------------------------------------------------
    #
    # Save:
    #
    # - Final report
    # - AI-generated summary
    # - Critic status
    # - Critic feedback
    # -----------------------------------------------------

    research.final_report = final_report

    # Save the AI-generated summary.
    research.summary = summary

    # Save the final Critic Agent decision.
    #
    # Example:
    #     PASS
    #     NEEDS IMPROVEMENT
    research.critic_status = (
        critic_result["status"]
    )

    # Save the Critic Agent feedback.
    research.critic_feedback = (
        critic_result["feedback"]
    )


    # -----------------------------------------------------
    # STEP 8: RESEARCH COMPLETED
    # -----------------------------------------------------

    research.status = "completed"

    research.save(
        update_fields=[
            "final_report",
            "summary",
            "critic_status",
            "critic_feedback",
            "status",
            "updated_at"
        ]
    )

    print(
        "STEP 8: Research workflow completed"
    )


    # -----------------------------------------------------
    # RETURN COMPLETE RESULT
    # -----------------------------------------------------

    return {
        "question": research.question,

        "search_results": (
            search_result["search_results"]
        ),

        "sources": (
            search_result["sources"]
        ),

        "scraped_results": (
            search_result["scraped_results"]
        ),

        "final_report": final_report,

        "summary": summary,

        "critic_result": critic_result
    }