/* ==========================================================
   RESEARCHAI
   PROGRESS PAGE JAVASCRIPT
========================================================== */

"use strict";


/* ==========================================================
   DJANGO API
========================================================== */

const API_BASE_URL =
    "http://127.0.0.1:8000";


/* ==========================================================
   GET RESEARCH ID
========================================================== */

const urlParams =
    new URLSearchParams(
        window.location.search
    );

const urlResearchId =
    urlParams.get("id");

const storedResearchId =
    sessionStorage.getItem(
        "research_id"
    );

const researchId =
    urlResearchId ||
    storedResearchId;


/* ==========================================================
   GET RESEARCH TOPIC
========================================================== */

const researchTopic =
    sessionStorage.getItem(
        "research_topic"
    );


/* ==========================================================
   CHECK RESEARCH ID
========================================================== */

if (!researchId) {

    console.error(
        "No research ID found."
    );

    window.location.href =
        "../index.html";
}


/* ==========================================================
   DOM ELEMENTS
========================================================== */

const progressStatusText =
    document.getElementById(
        "progressStatusText"
    );

const progressTitle =
    document.getElementById(
        "progressTitle"
    );

const activityTimeline =
    document.getElementById(
        "activityTimeline"
    );

const sourceCount =
    document.getElementById(
        "sourceCount"
    );

const sourceList =
    document.getElementById(
        "sourceList"
    );

const analysisStatus =
    document.getElementById(
        "analysisStatus"
    );


/* ==========================================================
   PIPELINE STEPS
========================================================== */

/*
    The visible frontend workflow is:

        Search
        Analyze Sources
        Write
        AI Review

    We intentionally do not show "Read" as a separate
    stage because reading/scraping is part of source
    analysis in our actual backend workflow.
*/

const pipelineSteps =
    document.querySelectorAll(
        ".pipeline-step"
    );


/* ==========================================================
   BACKEND STATUS → FRONTEND STEP
========================================================== */

/*
    Backend statuses:

        pending
        searching
        reading
        writing
        reviewing
        completed
        failed

    Frontend stages:

        search
        analyze
        write
        review

    "reading" is represented as "analyze" because the
    Search Agent performs the scraping and preparation
    of source information during this stage.
*/

function getStepFromStatus(status) {

    switch (status) {

        case "pending":
            return "search";


        case "searching":
            return "search";


        case "reading":
            return "analyze";


        case "writing":
            return "write";


        case "reviewing":
            return "review";


        case "completed":
            return "completed";


        case "failed":
            return "failed";


        default:
            return "search";
    }
}


/* ==========================================================
   STATUS TEXT
========================================================== */

function getStatusText(status) {

    switch (status) {

        case "pending":
            return "Preparing research";


        case "searching":
            return "Searching the web";


        case "reading":
            return "Analyzing research sources";


        case "writing":
            return "Writing research report";


        case "reviewing":
            return "AI reviewing research report";


        case "completed":
            return "Research completed";


        case "failed":
            return "Research failed";


        default:
            return "Research in Progress";
    }
}


/* ==========================================================
   TITLE TEXT
========================================================== */

function getTitleText(status) {

    switch (status) {

        case "pending":
            return "Preparing your research";


        case "searching":
            return "Finding relevant sources";


        case "reading":
            return "Analyzing the collected sources";


        case "writing":
            return "Writing your research report";


        case "reviewing":
            return "AI is reviewing your research report";


        case "completed":
            return "Your research is complete";


        case "failed":
            return "Research could not be completed";


        default:
            return "AI Agents are working on your research";
    }
}


/* ==========================================================
   ANALYSIS STATUS TEXT
========================================================== */

function getAnalysisText(status) {

    switch (status) {

        case "pending":
            return "Preparing research...";


        case "searching":
            return "Searching the web...";


        case "reading":
            return "Analyzing sources...";


        case "writing":
            return "Writing research report...";


        case "reviewing":
            return "AI reviewing report...";


        case "completed":
            return "Research complete";


        case "failed":
            return "Research failed";


        default:
            return "Processing...";
    }
}


/* ==========================================================
   UPDATE PIPELINE
========================================================== */

function updatePipeline(status) {

    const currentStep =
        getStepFromStatus(status);


    /* ------------------------------------------------------
       FAILED
    ------------------------------------------------------ */

    if (currentStep === "failed") {

        pipelineSteps.forEach(
            (step) => {

                step.classList.remove(
                    "active",
                    "current",
                    "completed"
                );

                const indicator =
                    step.querySelector(
                        ".step-indicator"
                    );

                if (indicator) {

                    indicator.textContent =
                        "!";
                }
            }
        );

        return;
    }


    /* ------------------------------------------------------
       COMPLETED
    ------------------------------------------------------ */

    if (currentStep === "completed") {

        pipelineSteps.forEach(
            (step) => {

                step.classList.remove(
                    "active",
                    "current"
                );

                step.classList.add(
                    "completed"
                );

                const indicator =
                    step.querySelector(
                        ".step-indicator"
                    );

                if (indicator) {

                    indicator.textContent =
                        "✓";
                }
            }
        );

        return;
    }


    /* ------------------------------------------------------
       STAGE ORDER
    ------------------------------------------------------ */

    const stepOrder = [
        "search",
        "analyze",
        "write",
        "review"
    ];


    const currentIndex =
        stepOrder.indexOf(
            currentStep
        );


    /* ------------------------------------------------------
       UPDATE EACH STAGE
    ------------------------------------------------------ */

    pipelineSteps.forEach(
        (step) => {

            const stepName =
                step.dataset.step;


            const stepIndex =
                stepOrder.indexOf(
                    stepName
                );


            /*
                Clear previous state.
            */

            step.classList.remove(
                "active",
                "current",
                "completed"
            );


            /*
                Earlier stages are completed.
            */

            if (
                stepIndex !== -1 &&
                stepIndex < currentIndex
            ) {

                step.classList.add(
                    "completed"
                );


                const indicator =
                    step.querySelector(
                        ".step-indicator"
                    );


                if (indicator) {

                    indicator.textContent =
                        "✓";
                }
            }


            /*
                Current stage is active.
            */

            else if (
                stepName === currentStep
            ) {

                step.classList.add(
                    "active"
                );

                step.classList.add(
                    "current"
                );
            }
        }
    );
}


/* ==========================================================
   ADD ACTIVITY
========================================================== */

function addActivity(message) {

    if (!activityTimeline) {
        return;
    }


    const activityItem =
        document.createElement(
            "div"
        );


    activityItem.className =
        "activity-item active";


    const currentTime =
        new Date().toLocaleTimeString(
            [],
            {
                hour: "2-digit",
                minute: "2-digit"
            }
        );


    /*
        Escape activity text before inserting it
        into the page.
    */

    const safeMessage =
        String(message)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");


    activityItem.innerHTML = `
        <time>${currentTime}</time>

        <span class="activity-dot"></span>

        <p>${safeMessage}</p>
    `;


    /*
        Previous activity entries are no longer active.
    */

    const previousItems =
        activityTimeline.querySelectorAll(
            ".activity-item"
        );


    previousItems.forEach(
        (item) => {

            item.classList.remove(
                "active"
            );
        }
    );


    activityTimeline.appendChild(
        activityItem
    );


    /*
        Keep the newest activity visible.
    */

    activityTimeline.scrollTop =
        activityTimeline.scrollHeight;
}


/* ==========================================================
   UPDATE ACTIVITY
========================================================== */

let lastStatus = null;


function updateActivity(status) {

    /*
        Polling runs every 2 seconds.

        Only create a new activity item when the
        backend status actually changes.
    */

    if (status === lastStatus) {
        return;
    }


    lastStatus = status;


    addActivity(
        getStatusText(status)
    );
}


/* ==========================================================
   RENDER SOURCES
========================================================== */

function updateSources(sources = []) {

    if (!sourceCount) {
        return;
    }


    /*
        The backend now returns saved ResearchSource
        objects through the "sources" field.
    */

    const totalSources =
        sources.length;


    /*
        The source counter shows how many sources have
        been collected.

        Example:

            5 / 5
    */

    sourceCount.textContent =
        `${totalSources} / ${totalSources}`;


    if (!sourceList) {
        return;
    }


    /*
        No sources yet.
    */

    if (!sources.length) {

        sourceList.innerHTML = `
            <p class="empty-state">
                Searching for reliable sources...
            </p>
        `;

        return;
    }


    /*
        Display the actual sources returned by Django.
    */

    sourceList.innerHTML =
        sources
            .map(
                (source) => {

                    const title =
                        String(
                            source.title ||
                            "Research Source"
                        )
                        .replaceAll("&", "&amp;")
                        .replaceAll("<", "&lt;")
                        .replaceAll(">", "&gt;")
                        .replaceAll('"', "&quot;")
                        .replaceAll("'", "&#039;");


                    const url =
                        String(
                            source.url ||
                            ""
                        )
                        .replaceAll("&", "&amp;")
                        .replaceAll("<", "&lt;")
                        .replaceAll(">", "&gt;")
                        .replaceAll('"', "&quot;")
                        .replaceAll("'", "&#039;");


                    return `
                        <div class="source-item">

                            <span class="source-status">
                                ✓
                            </span>

                            <div class="source-information">

                                <strong>
                                    ${title}
                                </strong>

                                <span>
                                    ${url}
                                </span>

                            </div>

                        </div>
                    `;
                }
            )
            .join("");
}


/* ==========================================================
   UPDATE PAGE
========================================================== */

function updatePage(data) {

    const status =
        data.status;


    /*
        Update status label.
    */

    if (progressStatusText) {

        progressStatusText.textContent =
            getStatusText(status);
    }


    /*
        Update main heading.
    */

    if (progressTitle) {

        progressTitle.textContent =
            getTitleText(status);
    }


    /*
        Update bottom activity message.
    */

    if (analysisStatus) {

        analysisStatus.textContent =
            getAnalysisText(status);
    }


    /*
        Update pipeline.
    */

    updatePipeline(
        status
    );


    /*
        Update Current Activity.
    */

    updateActivity(
        status
    );


    /*
        Update actual sources returned
        by the Django API.
    */

    updateSources(
        data.sources || []
    );
}


/* ==========================================================
   FETCH RESEARCH STATUS
========================================================== */

async function fetchResearchStatus() {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/api/research/${encodeURIComponent(
                    researchId
                )}/`
            );


        /*
            Check HTTP response.
        */

        if (!response.ok) {

            throw new Error(
                `Status request failed: ${response.status}`
            );
        }


        /*
            Convert API response to JSON.
        */

        const data =
            await response.json();


        console.log(
            "Research status:",
            data.status
        );


        /*
            Also log source count so we can
            debug the Progress Page easily.
        */

        console.log(
            "Sources:",
            data.sources?.length || 0
        );


        /*
            Update the page.
        */

        updatePage(
            data
        );


        /*
            Stop polling when the workflow ends.
        */

        if (
            data.status === "completed" ||
            data.status === "failed"
        ) {

            stopPolling();


            /*
                Give the user a short moment to see
                the completed state.
            */

            if (
                data.status === "completed"
            ) {

                setTimeout(
                    () => {

                        window.location.href =
                            `report.html?id=${encodeURIComponent(
                                researchId
                            )}`;

                    },
                    1200
                );
            }
        }

    }

    catch (error) {

        console.error(
            "PROGRESS ERROR:",
            error
        );
    }
}


/* ==========================================================
   POLLING
========================================================== */

let pollingInterval = null;


function startPolling() {

    /*
        Fetch immediately.
    */

    fetchResearchStatus();


    /*
        Continue checking every 2 seconds.
    */

    pollingInterval =
        setInterval(
            fetchResearchStatus,
            2000
        );
}


/* ==========================================================
   STOP POLLING
========================================================== */

function stopPolling() {

    if (pollingInterval) {

        clearInterval(
            pollingInterval
        );

        pollingInterval = null;
    }
}


/* ==========================================================
   INITIALIZE PAGE
========================================================== */

if (researchId) {

    console.log(
        "Monitoring research:",
        researchId
    );


    /*
        Display the research topic if the HTML
        contains an element for it.
    */

    const topicElement =
        document.getElementById(
            "researchTopicDisplay"
        );


    if (
        topicElement &&
        researchTopic
    ) {

        topicElement.textContent =
            researchTopic;
    }


    /*
        Start monitoring the backend.
    */

    startPolling();
}