# ---------------------------------------------------------
# RESEARCH VIEWS
# ---------------------------------------------------------
# This file contains the API endpoints for our ResearchAI
# application.
#
# The API is responsible for:
#
# 1. Receiving research questions.
# 2. Creating Research records in PostgreSQL.
# 3. Starting the AI research workflow in the background.
# 4. Updating the research status.
# 5. Returning the Research ID immediately.
# 6. Generating and downloading research reports as PDF.
#
# IMPORTANT:
#
# Previously, the POST API waited for the complete AI
# workflow before responding to the frontend.
#
# That caused:
#
# Frontend
#     ↓
# POST request
#     ↓
# Search
#     ↓
# Scraping
#     ↓
# Writer
#     ↓
# Critic
#     ↓
# Response
#
# This could take a long time.
#
# Now:
#
# Frontend
#     ↓
# POST request
#     ↓
# Create Research
#     ↓
# Start background thread
#     ↓
# Return Research ID immediately
#
# Meanwhile, the AI workflow continues in the background.
# ---------------------------------------------------------


# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

from threading import Thread

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.http import FileResponse

from .models import Research
from .serializers import ResearchSerializer
from .services import process_research
from .pdf_service import generate_research_pdf


# ---------------------------------------------------------
# BACKGROUND RESEARCH FUNCTION
# ---------------------------------------------------------

def run_research_in_background(research_id):
    """
    Run the complete ResearchAI workflow in a background
    thread.

    Parameters:
        research_id:
            ID of the Research record stored in PostgreSQL.

    Why do we use the ID?

    The API request creates the Research object first.
    The background thread then retrieves the latest version
    of that object from the database.

    This allows services.py to update the status:

        searching
        reading
        writing
        reviewing
        completed

    If something fails, the status becomes:

        failed
    """

    try:

        # -------------------------------------------------
        # GET RESEARCH OBJECT
        # -------------------------------------------------
        # Retrieve the Research record from PostgreSQL.
        # -------------------------------------------------

        research = Research.objects.get(
            id=research_id
        )

        print(
            f"BACKGROUND: Starting research {research_id}"
        )


        # -------------------------------------------------
        # RUN THE COMPLETE AI WORKFLOW
        # -------------------------------------------------
        # services.py is now responsible for:
        #
        # Search Agent
        #      ↓
        # Reading / Scraping
        #      ↓
        # Writer Agent
        #      ↓
        # Critic Agent
        #      ↓
        # Optional Revision
        #      ↓
        # Completed
        # -------------------------------------------------

        process_research(
            research
        )


        print(
            f"BACKGROUND: Research {research_id} completed"
        )


    except Research.DoesNotExist:

        # -------------------------------------------------
        # RESEARCH RECORD WAS NOT FOUND
        # -------------------------------------------------

        print(
            f"BACKGROUND ERROR: Research {research_id} "
            "does not exist."
        )


    except Exception as e:

        # -------------------------------------------------
        # HANDLE BACKGROUND WORKFLOW FAILURE
        # -------------------------------------------------
        # If Search, Scraping, Writer, Critic, or another
        # part of the workflow fails, mark the research as
        # failed.
        # -------------------------------------------------

        try:

            research = Research.objects.get(
                id=research_id
            )

            research.status = "failed"

            research.save(
                update_fields=[
                    "status",
                    "updated_at"
                ]
            )

        except Research.DoesNotExist:

            # If the Research object itself no longer exists,
            # there is nothing to update.
            pass


        # Print the error in the Django terminal so we can
        # diagnose problems during development.

        print(
            f"BACKGROUND ERROR: Research {research_id}: {e}"
        )


# ---------------------------------------------------------
# TEST API
# ---------------------------------------------------------

@api_view(["GET"])
def test_api(request):
    """
    Simple endpoint used to check whether the
    ResearchAI API is working.
    """

    return Response({
        "message": "ResearchAI API is working!"
    })


# ---------------------------------------------------------
# RESEARCH API
# ---------------------------------------------------------

@api_view(["GET", "POST"])
def create_research(request):
    """
    Handle research requests.

    GET:
        Return all Research records.

    POST:
        1. Validate the user's question.
        2. Create a Research database record.
        3. Start the AI workflow in the background.
        4. Return the Research ID immediately.
    """

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------
    # Return all research records stored in PostgreSQL.
    # -----------------------------------------------------

    if request.method == "GET":

        researches = Research.objects.all()

        serializer = ResearchSerializer(
            researches,
            many=True
        )

        return Response(
            serializer.data
        )


    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------
    # Create a new research request.
    # -----------------------------------------------------

    if request.method == "POST":

        # -------------------------------------------------
        # VALIDATE USER INPUT
        # -------------------------------------------------
        # The serializer checks whether the incoming JSON
        # contains valid Research data.
        # -------------------------------------------------

        serializer = ResearchSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


        # -------------------------------------------------
        # CREATE RESEARCH DATABASE RECORD
        # -------------------------------------------------
        # Because the model's default status is "pending",
        # a new Research object initially has:
        #
        # status = "pending"
        # -------------------------------------------------

        research = serializer.save()


        # -------------------------------------------------
        # START BACKGROUND THREAD
        # -------------------------------------------------
        # IMPORTANT:
        #
        # DO NOT do this:
        #
        # process_research(research)
        #
        # directly inside the API request.
        #
        # That would make the browser wait for the entire
        # research workflow.
        #
        # Instead, create a background thread.
        # -------------------------------------------------

        thread = Thread(
            target=run_research_in_background,
            args=(research.id,)
        )


        # -------------------------------------------------
        # DAEMON THREAD
        # -------------------------------------------------
        # This tells Python that this background thread
        # should not prevent the Django development process
        # from shutting down.
        # -------------------------------------------------

        thread.daemon = True


        # -------------------------------------------------
        # START BACKGROUND WORK
        # -------------------------------------------------

        thread.start()


        # -------------------------------------------------
        # RETURN RESPONSE IMMEDIATELY
        # -------------------------------------------------
        # The AI workflow is still running in the background.
        #
        # The frontend does NOT wait for:
        #
        # Search
        # Scraping
        # Writer
        # Critic
        #
        # Instead, it receives the Research ID and can
        # immediately navigate to the Progress Page.
        # -------------------------------------------------

        response_serializer = ResearchSerializer(
            research
        )

        return Response(
            {
                "message": "Research started.",
                "research": response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


# ---------------------------------------------------------
# SINGLE RESEARCH API
# ---------------------------------------------------------

@api_view(["GET", "PUT", "DELETE"])
def get_research(request, id):
    """
    Handle one specific Research record.

    GET:
        Return the research record.

    PUT:
        Update the research record.

    DELETE:
        Delete the research record.
    """

    # -----------------------------------------------------
    # FIND RESEARCH
    # -----------------------------------------------------

    try:

        research = Research.objects.get(
            id=id
        )

    except Research.DoesNotExist:

        return Response(
            {
                "error": "Research not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )


    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------
    # The Progress Page will use this endpoint later to
    # check the current research status.
    #
    # Example:
    #
    # GET /api/research/5/
    #
    # Response:
    #
    # {
    #     "id": 5,
    #     "question": "AI in agriculture",
    #     "status": "searching"
    # }
    # -----------------------------------------------------

    if request.method == "GET":

        serializer = ResearchSerializer(
            research
        )

        return Response(
            serializer.data
        )


    # -----------------------------------------------------
    # PUT
    # -----------------------------------------------------
    # Update an existing research record.
    # -----------------------------------------------------

    if request.method == "PUT":

        serializer = ResearchSerializer(
            research,
            data=request.data
        )

        if serializer.is_valid():

            research = serializer.save()

            response_serializer = ResearchSerializer(
                research
            )

            return Response(
                response_serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    # -----------------------------------------------------
    # DELETE
    # -----------------------------------------------------
    # Delete the research record.
    # -----------------------------------------------------

    if request.method == "DELETE":

        research.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


# ---------------------------------------------------------
# DOWNLOAD RESEARCH PDF
# ---------------------------------------------------------

@api_view(["GET"])
def download_research_pdf(request, id):
    """
    Generate and download the completed research report
    as a PDF file.
    """

    # -----------------------------------------------------
    # FIND RESEARCH
    # -----------------------------------------------------

    try:

        research = Research.objects.get(
            id=id
        )

    except Research.DoesNotExist:

        return Response(
            {
                "error": "Research not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )


    # -----------------------------------------------------
    # CHECK RESEARCH STATUS
    # -----------------------------------------------------
    # PDF can only be generated after the research
    # workflow has completed.
    # -----------------------------------------------------

    if research.status != "completed":

        return Response(
            {
                "error": "Research report is not completed yet."
            },
            status=status.HTTP_400_BAD_REQUEST
        )


    # -----------------------------------------------------
    # CHECK REPORT CONTENT
    # -----------------------------------------------------

    if not research.final_report.strip():

        return Response(
            {
                "error": "Research report is empty."
            },
            status=status.HTTP_400_BAD_REQUEST
        )


    # -----------------------------------------------------
    # GENERATE PDF
    # -----------------------------------------------------

    pdf_buffer = generate_research_pdf(
        research
    )


    # -----------------------------------------------------
    # RETURN PDF TO BROWSER
    # -----------------------------------------------------

    return FileResponse(
        pdf_buffer,
        as_attachment=True,
        filename="research-report.pdf",
        content_type="application/pdf"
    )