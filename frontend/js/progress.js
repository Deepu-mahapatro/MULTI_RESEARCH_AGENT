"use strict";


/*
    ============================================
    CONFIGURATION
    ============================================
*/

const API_BASE_URL =
    "http://127.0.0.1:8000";


/*
    ============================================
    GET RESEARCH ID
    ============================================
*/

const urlParams =
    new URLSearchParams(window.location.search);

const researchId =
    urlParams.get("id") ||
    sessionStorage.getItem("research_id");


/*
    ============================================
    DOM ELEMENTS
    ============================================
*/

const sourceCount =
    document.getElementById("sourceCount");

const sourceList =
    document.getElementById("sourceList");

const activityTimeline =
    document.getElementById("activityTimeline");

const analysisStatus =
    document.getElementById("analysisStatus");

const currentActivity =
    document.getElementById("currentActivity");


/*
    ============================================
    POLLING CONTROL
    ============================================
*/

let pollingInterval = null;

let lastStatus = null;


/*
    ============================================
    PIPELINE STAGES
    ============================================
*/

const pipelineStages = [
    "search",
    "analyze",
    "write",
    "review"
];


/*
    ============================================
    STAGE NUMBERS
    ============================================
*/

const stageNumbers = {
    search: "1",
    analyze: "2",
    write: "3",
    review: "4"
};


/*
    ============================================
    STATUS MAPPING
    ============================================
*/

function getStageFromStatus(status) {

    if (
        status === "pending" ||
        status === "searching"
    ) {
        return "search";
    }

    if (status === "reading") {
        return "analyze";
    }

    if (status === "writing") {
        return "write";
    }

    if (status === "reviewing") {
        return "review";
    }

    if (status === "completed") {
        return "completed";
    }

    if (status === "failed") {
        return "failed";
    }

    return "search";
}


/*
    ============================================
    USER-FRIENDLY STATUS TEXT
    ============================================
*/

function getStatusText(status) {

    if (
        status === "pending"
    ) {
        return "Preparing research...";
    }

    if (
        status === "searching"
    ) {
        return "Searching the web...";
    }

    if (
        status === "reading"
    ) {
        return "Analyzing research sources...";
    }

    if (
        status === "writing"
    ) {
        return "Writing the research report...";
    }

    if (
        status === "reviewing"
    ) {
        return "Reviewing the research report...";
    }

    if (
        status === "completed"
    ) {
        return "Research completed successfully.";
    }

    if (
        status === "failed"
    ) {
        return "Research failed.";
    }

    return "Processing research...";
}


/*
    ============================================
    ESCAPE HTML
    ============================================
*/

function escapeHTML(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/*
    ============================================
    UPDATE PIPELINE
    ============================================
*/

function updatePipeline(status) {

    const currentStage =
        getStageFromStatus(status);


    /*
        progress.html uses:

            data-step="search"
            data-step="analyze"
            data-step="write"
            data-step="review"

        Therefore JavaScript searches
        for [data-step].
    */

    const stageElements =
        document.querySelectorAll(
            "[data-step]"
        );


    let currentIndex =
        pipelineStages.indexOf(currentStage);


    /*
        When research is completed,
        all four stages become completed.
    */

    if (currentStage === "completed") {

        currentIndex =
            pipelineStages.length;
    }


    /*
        Update every pipeline stage.
    */

    stageElements.forEach(
        (element) => {

            const stage =
                element.dataset.step;


            const stageIndex =
                pipelineStages.indexOf(stage);


            /*
                Get the indicator inside
                the current pipeline stage.

                Example:

                    <div class="step-indicator">
                        2
                    </div>
            */

            const indicator =
                element.querySelector(
                    ".step-indicator"
                );


            /*
                Remove old states first.

                This prevents an old
                active/completed state
                from remaining incorrectly.
            */

            element.classList.remove(
                "active",
                "completed"
            );


            /*
                ==================================
                COMPLETED RESEARCH
                ==================================
            */

            if (
                currentStage === "completed"
            ) {

                element.classList.add(
                    "completed"
                );


                /*
                    Change the indicator
                    to a checkmark.
                */

                if (indicator) {

                    indicator.textContent =
                        "✓";
                }
            }


            /*
                ==================================
                PREVIOUS COMPLETED STAGES
                ==================================
            */

            else if (
                stageIndex < currentIndex
            ) {

                element.classList.add(
                    "completed"
                );


                /*
                    Change the completed stage
                    number to a checkmark.
                */

                if (indicator) {

                    indicator.textContent =
                        "✓";
                }
            }


            /*
                ==================================
                CURRENT ACTIVE STAGE
                ==================================
            */

            else if (
                stage === currentStage
            ) {

                element.classList.add(
                    "active"
                );


                /*
                    Keep the current stage number.
                */

                if (indicator) {

                    indicator.textContent =
                        stageNumbers[stage];
                }
            }


            /*
                ==================================
                FUTURE STAGES
                ==================================
            */

            else {

                /*
                    Restore the original
                    stage number.

                    Example:

                        Analyze → 2
                        Write   → 3
                        Review  → 4
                */

                if (indicator) {

                    indicator.textContent =
                        stageNumbers[stage];
                }
            }
        }
    );
}


/*
    ============================================
    UPDATE CURRENT ACTIVITY
    ============================================
*/

function updateCurrentActivity(status) {

    if (!currentActivity) {
        return;
    }

    currentActivity.textContent =
        getStatusText(status);
}


/*
    ============================================
    UPDATE BOTTOM STATUS
    ============================================
*/

function updateAnalysisStatus(status) {

    if (!analysisStatus) {
        return;
    }

    analysisStatus.textContent =
        getStatusText(status);
}


/*
    ============================================
    ADD ACTIVITY TO TIMELINE
    ============================================
*/

function addActivity(status) {

    if (!activityTimeline) {
        return;
    }


    const activityText =
        getStatusText(status);


    const item =
        document.createElement("div");


    item.className =
        "activity-item";


    item.innerHTML = `
        <div class="activity-dot"></div>

        <div class="activity-content">
            ${escapeHTML(activityText)}
        </div>
    `;


    activityTimeline.appendChild(item);
}


/*
    ============================================
    UPDATE SOURCE LIST
    ============================================
*/

function updateSources(sources) {

    if (!sourceList || !sourceCount) {
        return;
    }


    if (!Array.isArray(sources)) {

        sourceCount.textContent = "0";

        sourceList.innerHTML =
            "<p>No sources available yet.</p>";

        return;
    }


    sourceCount.textContent =
        sources.length;


    if (sources.length === 0) {

        sourceList.innerHTML =
            "<p>No sources available yet.</p>";

        return;
    }


    sourceList.innerHTML =
        sources
            .map(
                (source) => {

                    const title =
                        source.title ||
                        "Research Source";


                    const url =
                        source.url ||
                        "#";


                    return `
                        <div class="source-item">

                            <div class="source-title">
                                ${escapeHTML(title)}
                            </div>

                            <div class="source-url">
                                ${escapeHTML(url)}
                            </div>

                        </div>
                    `;
                }
            )
            .join("");
}


/*
    ============================================
    STOP POLLING
    ============================================
*/

function stopPolling() {

    if (pollingInterval) {

        clearInterval(
            pollingInterval
        );

        pollingInterval = null;
    }
}


/*
    ============================================
    FETCH RESEARCH STATUS
    ============================================
*/

async function fetchResearchStatus() {

    if (!researchId) {

        console.error(
            "Research ID not found."
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/api/research/${researchId}/`
            );


        if (!response.ok) {

            throw new Error(
                `HTTP error: ${response.status}`
            );
        }


        const data =
            await response.json();


        console.log(
            "Research status:",
            data
        );


        /*
            Update pipeline.
        */

        updatePipeline(
            data.status
        );


        /*
            Update current activity.
        */

        updateCurrentActivity(
            data.status
        );


        /*
            Update bottom status.
        */

        updateAnalysisStatus(
            data.status
        );


        /*
            Update sources.
        */

        updateSources(
            data.sources
        );


        /*
            Add activity only when
            the status changes.
        */

        if (
            data.status !== lastStatus
        ) {

            addActivity(
                data.status
            );

            lastStatus =
                data.status;
        }


        /*
            ========================================
            RESEARCH COMPLETION
            ========================================

            Stop polling when the workflow ends.
        */

        if (
            data.status === "completed" ||
            data.status === "failed"
        ) {

            stopPolling();


            /*
                Research completed successfully.

                Send a custom Google Analytics event
                so we can measure how many research
                requests actually finish successfully.
            */

            if (
                data.status === "completed"
            ) {

                // Track completed research.
                if (
                    typeof gtag === "function"
                ) {

                    gtag(
                        "event",
                        "research_completed"
                    );


                    console.log(
                        "Google Analytics event sent: research_completed"
                    );

                }
                else {

                    console.warn(
                        "Google Analytics gtag function is not available."
                    );
                }


                /*
                    Give the user a short moment
                    to see the completed state
                    before opening the final report.
                */

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
            "STATUS FETCH ERROR:",
            error
        );
    }
}


/*
    ============================================
    START POLLING
    ============================================
*/

function startPolling() {

    fetchResearchStatus();


    pollingInterval =
        setInterval(
            fetchResearchStatus,
            2000
        );
}


/*
    ============================================
    PAGE INITIALIZATION
    ============================================
*/

document.addEventListener(
    "DOMContentLoaded",
    () => {

        if (!researchId) {

            console.error(
                "No research ID found."
            );


            if (analysisStatus) {

                analysisStatus.textContent =
                    "Research ID not found.";
            }


            return;
        }


        console.log(
            "Starting research progress...",
            researchId
        );


        startPolling();
    }
);