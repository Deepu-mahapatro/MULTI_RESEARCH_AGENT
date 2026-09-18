# ---------------------------------------------------------
# SEARCH AGENT
# ---------------------------------------------------------
# The Search Agent is responsible for:
#
# 1. Searching the web using Tavily.
# 2. Extracting URLs from the search results.
# 3. Scraping useful webpages concurrently.
# 4. Handling webpages that cannot be scraped.
# 5. Returning the collected research information.
#
# We also keep structured source information so that later
# the Report Page can display the actual sources used.
# ---------------------------------------------------------


# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

import re

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from research.tools import (
    web_search,
    scrape_url
)


# ---------------------------------------------------------
# SCRAPE ONE URL
# ---------------------------------------------------------

def scrape_single_url(url):
    """
    Scrape one webpage.

    Returns:
        {
            "url": url,
            "content": content
        }

    Returns None if scraping fails.
    """

    scraped_content = scrape_url.invoke(url)


    # -----------------------------------------------------
    # CHECK FOR SCRAPING FAILURE
    # -----------------------------------------------------

    if scraped_content.startswith(
        "Could not scrape URL:"
    ):
        return None


    # -----------------------------------------------------
    # CHECK FOR EMPTY CONTENT
    # -----------------------------------------------------

    if not scraped_content.strip():
        return None


    # -----------------------------------------------------
    # RETURN SUCCESSFUL RESULT
    # -----------------------------------------------------

    return {
        "url": url,
        "content": scraped_content
    }


# ---------------------------------------------------------
# SEARCH AGENT
# ---------------------------------------------------------

def run_search_agent(question):
    """
    Run the Search Agent.

    Workflow:

        Question
            ↓
        Tavily Search
            ↓
        Extract URLs
            ↓
        Concurrent Scraping
            ↓
        Research Information
    """


    # -----------------------------------------------------
    # STEP 1: SEARCH TAVILY
    # -----------------------------------------------------

    print(
        "SEARCH AGENT: Searching Tavily..."
    )

    search_results = web_search.invoke(
        question
    )

    print(
        "SEARCH AGENT: Tavily search completed"
    )


    # -----------------------------------------------------
    # STEP 2: EXTRACT URLs
    # -----------------------------------------------------
    #
    # We are intentionally using the same URL extraction
    # approach that worked in our original Search Agent.
    #
    # Example:
    #
    # URL: https://example.com/article
    #
    # becomes:
    #
    # https://example.com/article
    # -----------------------------------------------------

    urls = re.findall(
        r"URL:\s*(https?://\S+)",
        search_results
    )


    print(
        f"SEARCH AGENT: Found {len(urls)} URLs"
    )


    # -----------------------------------------------------
    # STEP 3: LIMIT SCRAPING
    # -----------------------------------------------------
    #
    # We scrape only the first 3 URLs.
    #
    # However, all search results are still preserved in
    # the original search_results string.
    # -----------------------------------------------------

    urls_to_scrape = urls[:3]


    # -----------------------------------------------------
    # STEP 4: CREATE STRUCTURED SOURCES
    # -----------------------------------------------------
    #
    # For now we extract titles from the search result
    # blocks where possible.
    #
    # This data will later be stored in PostgreSQL.
    # -----------------------------------------------------

    sources = []


    for url in urls:

        title = "Research Source"


        # Try to find the title immediately before the URL.
        url_position = search_results.find(url)


        if url_position != -1:

            previous_text = search_results[
                max(
                    0,
                    url_position - 500
                ):url_position
            ]


            title_match = re.findall(
                r"Title:\s*(.+)",
                previous_text
            )


            if title_match:

                title = title_match[-1].strip()


        sources.append({
            "title": title,
            "url": url
        })


    # -----------------------------------------------------
    # STEP 5: SCRAPE CONCURRENTLY
    # -----------------------------------------------------
    #
    # Instead of:
    #
    # URL 1 → wait
    # URL 2 → wait
    # URL 3 → wait
    #
    # we now do:
    #
    # URL 1 ─┐
    # URL 2 ─┼→ run at the same time
    # URL 3 ─┘
    # -----------------------------------------------------

    scraped_results = []


    if urls_to_scrape:

        print(
            "SEARCH AGENT: Scraping "
            f"{len(urls_to_scrape)} sources concurrently..."
        )


        with ThreadPoolExecutor(
            max_workers=3
        ) as executor:

            future_to_url = {
                executor.submit(
                    scrape_single_url,
                    url
                ): url

                for url in urls_to_scrape
            }


            for future in as_completed(
                future_to_url
            ):

                url = future_to_url[future]


                try:

                    result = future.result()


                    if result is not None:

                        scraped_results.append(
                            result
                        )

                        print(
                            "SEARCH AGENT: Scraped:",
                            url
                        )

                    else:

                        print(
                            "SEARCH AGENT: Skipped:",
                            url
                        )


                except Exception as e:

                    print(
                        "SEARCH AGENT: Scraping error:",
                        url,
                        e
                    )

    else:

        print(
            "SEARCH AGENT: No URLs found to scrape."
        )


    # -----------------------------------------------------
    # STEP 6: RETURN RESULTS
    # -----------------------------------------------------

    print(
        "SEARCH AGENT: "
        f"Successfully scraped "
        f"{len(scraped_results)} sources"
    )

    print(
        "SEARCH AGENT: Completed"
    )


    return {
        "question": question,

        "search_results": search_results,

        "sources": sources,

        "scraped_results": scraped_results
    }