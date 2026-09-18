# ---------------------------------------------------------
# RESEARCH TOOLS
# ---------------------------------------------------------
# This file contains the tools used by our ResearchAI
# research system.
#
# Currently we have two tools:
#
# 1. web_search()
#       Searches the internet using Tavily.
#
# 2. scrape_url()
#       Downloads a webpage and extracts readable text
#       using Requests and BeautifulSoup.
#
# These tools will later be used by our Search Agent.
# ---------------------------------------------------------


# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

# LangChain's @tool decorator allows our Python
# functions to be used as LangChain tools.
from langchain.tools import tool

# Requests is used to send HTTP requests and download
# webpages from URLs.
import requests

# BeautifulSoup is used to parse HTML and extract
# readable information from webpages.
from bs4 import BeautifulSoup

# TavilyClient allows our application to perform
# web searches through the Tavily API.
from tavily import TavilyClient

# os allows us to read environment variables.
import os

# load_dotenv loads variables from our .env file.
from dotenv import load_dotenv


# Load environment variables from .env.
load_dotenv()


# ---------------------------------------------------------
# TAVILY CLIENT
# ---------------------------------------------------------

# Create the Tavily client using the API key stored
# inside the .env file.
#
# We never hard-code the API key in this file.
tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


# ---------------------------------------------------------
# WEB SEARCH TOOL
# ---------------------------------------------------------

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information
    on a topic.

    Returns titles, URLs and snippets.
    """

    # Send the research question to Tavily.
    results = tavily.search(
        query=query,
        max_results=5
    )

    # Store formatted search results.
    out = []

    # Process every result returned by Tavily.
    for r in results["results"]:

        out.append(
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content'][:300]}\n"
        )

    # Return all results as one string.
    return "\n-----\n".join(out)


# ---------------------------------------------------------
# SCRAPE URL TOOL
# ---------------------------------------------------------

@tool
def scrape_url(url: str) -> str:
    """
    Scrape and return clean text content from a webpage.

    The function:

    1. Downloads the webpage.
    2. Checks HTTP errors.
    3. Parses HTML with BeautifulSoup.
    4. Removes unnecessary HTML elements.
    5. Extracts readable text.
    6. Detects obvious blocked/error pages.
    7. Limits content to 3000 characters.
    """

    try:

        # -------------------------------------------------
        # STEP 1: DOWNLOAD THE WEBPAGE
        # -------------------------------------------------

        response = requests.get(
            url,
            timeout=8,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )


        # -------------------------------------------------
        # STEP 2: CHECK HTTP STATUS
        # -------------------------------------------------

        # This detects HTTP errors such as:
        #
        # 403 → Forbidden
        # 404 → Not Found
        # 500 → Server Error
        #
        # Important:
        # Some websites return HTTP 200 even when they
        # display an error page. That is why we also have
        # the error-indicator check below.
        response.raise_for_status()


        # -------------------------------------------------
        # STEP 3: PARSE HTML
        # -------------------------------------------------

        # Give the downloaded HTML to BeautifulSoup.
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        # -------------------------------------------------
        # STEP 4: REMOVE UNNECESSARY ELEMENTS
        # -------------------------------------------------

        # These elements normally aren't useful for
        # research:
        #
        # script → JavaScript
        # style  → CSS
        # nav    → navigation
        # footer → footer information
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer"
        ]):
            tag.decompose()


        # -------------------------------------------------
        # STEP 5: EXTRACT READABLE TEXT
        # -------------------------------------------------

        clean_text = soup.get_text(
            separator=" ",
            strip=True
        )


        # -------------------------------------------------
        # STEP 6: DETECT BLOCKED/ERROR PAGES
        # -------------------------------------------------

        # Some websites return HTTP 200 but actually
        # return an error or anti-bot page.
        #
        # We encountered this with ScienceDirect,
        # which returned a Cloudflare error page.
        error_indicators = [
            "cloudflare_error",
            "there was a problem providing the content",
            "access denied",
            "captcha",
            "verify you are human",
            "temporarily unavailable"
        ]


        # Convert the webpage text to lowercase.
        lower_text = clean_text.lower()


        # Check every known error indicator.
        for error_message in error_indicators:

            if error_message in lower_text:

                return (
                    "Could not scrape URL: "
                    "webpage appears to be blocked or "
                    f"unavailable ({error_message})."
                )


        # -------------------------------------------------
        # STEP 7: CHECK FOR EMPTY CONTENT
        # -------------------------------------------------

        if not clean_text:

            return (
                "Could not scrape URL: "
                "no readable content found."
            )


        # -------------------------------------------------
        # STEP 8: LIMIT CONTENT SIZE
        # -------------------------------------------------

        # Return only the first 3000 characters so that
        # one webpage does not create too much data.
        return clean_text[:3000]


    # -----------------------------------------------------
    # STEP 9: HANDLE ERRORS
    # -----------------------------------------------------

    # If anything unexpected happens, return a clear
    # error message instead of crashing the application.
    except Exception as e:

        return f"Could not scrape URL: {str(e)}"