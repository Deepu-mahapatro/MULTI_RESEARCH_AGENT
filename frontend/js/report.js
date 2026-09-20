/* ==========================================================
   RESEARCHAI
   FINAL REPORT JAVASCRIPT
========================================================== */

"use strict";


/* ==========================================================
   CONFIGURATION
========================================================== */

const API_BASE_URL =
    "https://multi-research-agent-luez.onrender.com";


/* ==========================================================
   GET RESEARCH ID
========================================================== */

const reportParams =
    new URLSearchParams(
        window.location.search
    );

const reportResearchId =
    reportParams.get("id") ||
    sessionStorage.getItem(
        "research_id"
    );


/* ==========================================================
   DOM ELEMENTS
========================================================== */

const reportTitle =
    document.getElementById(
        "reportTitle"
    );

const reportDate =
    document.getElementById(
        "reportDate"
    );

const reportContent =
    document.getElementById(
        "reportContent"
    );

const sourceTotal =
    document.getElementById(
        "sourceTotal"
    );

const wordTotal =
    document.getElementById(
        "wordTotal"
    );

const reviewScore =
    document.getElementById(
        "reviewScore"
    );

const sourceReliability =
    document.getElementById(
        "sourceReliability"
    );

const topSourcesList =
    document.getElementById(
        "topSourcesList"
    );

const allSources =
    document.getElementById(
        "allSources"
    );

const reviewContent =
    document.getElementById(
        "reviewContent"
    );

const summaryContent =
    document.getElementById(
        "summaryContent"
    );


/* ==========================================================
   HTML SAFETY
========================================================== */

function escapeHTML(value = "") {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


/* ==========================================================
   SOURCE RELIABILITY
========================================================== */

function calculateSourceReliability(
    sources = []
) {

    if (!sources.length) {

        return "—";
    }


    let highTrust = 0;

    let mediumTrust = 0;

    let lowTrust = 0;


    sources.forEach(
        (source) => {

            try {

                if (!source.url) {

                    lowTrust++;

                    return;
                }


                const url =
                    new URL(
                        source.url
                    );


                const hostname =
                    url.hostname
                        .toLowerCase()
                        .replace(
                            /^www\./,
                            ""
                        );


                const isHighTrust =
                    hostname.endsWith(".gov") ||
                    hostname.endsWith(".gov.in") ||
                    hostname.endsWith(".edu") ||
                    hostname.endsWith(".edu.in") ||
                    hostname === "who.int" ||
                    hostname.endsWith(".who.int") ||
                    hostname === "un.org" ||
                    hostname.endsWith(".un.org") ||
                    hostname.endsWith(".ieee.org") ||
                    hostname.endsWith(".acm.org") ||
                    hostname === "wikipedia.org" ||
                    hostname.endsWith(".wikipedia.org");


                const isMediumTrust =
                    hostname.endsWith(".org") ||
                    hostname.includes("mozilla.org") ||
                    hostname.includes("microsoft.com") ||
                    hostname.includes("google.com") ||
                    hostname.includes("aws.amazon.com") ||
                    hostname.includes("cloud.google.com") ||
                    hostname.includes("github.com") ||
                    hostname.includes("redhat.com") ||
                    hostname.includes("ibm.com") ||
                    hostname.includes("oracle.com") ||
                    hostname.includes("geeksforgeeks.org") ||
                    hostname.includes("w3schools.com");


                if (isHighTrust) {

                    highTrust++;

                } else if (isMediumTrust) {

                    mediumTrust++;

                } else {

                    lowTrust++;
                }

            } catch {

                lowTrust++;
            }
        }
    );


    const total =
        highTrust +
        mediumTrust +
        lowTrust;


    if (total === 0) {

        return "—";
    }


    const highRatio =
        highTrust / total;


    const combinedRatio =
        (
            highTrust +
            mediumTrust
        ) / total;


    if (highRatio >= 0.5) {

        return "High";
    }


    if (combinedRatio >= 0.5) {

        return "Medium";
    }


    return "Low";
}


/* ==========================================================
   REPORT RENDERING
========================================================== */

function renderReport(
    reportText = ""
) {

    if (!reportContent) {

        return;
    }


    const sections =
        String(reportText)
            .split(/\n\s*\n/)
            .map(
                (section) =>
                    section.trim()
            )
            .filter(Boolean);


    if (!sections.length) {

        reportContent.innerHTML = `
            <p class="empty-state">
                No report content available.
            </p>
        `;

        return;
    }


    reportContent.innerHTML =
        sections
            .map(
                (section) => {

                    let safeText =
                        escapeHTML(
                            section
                        );


                    safeText =
                        safeText.replace(
                            /^### (.+)$/gm,
                            "<h4>$1</h4>"
                        );


                    safeText =
                        safeText.replace(
                            /^## (.+)$/gm,
                            "<h3>$1</h3>"
                        );


                    safeText =
                        safeText.replace(
                            /^# (.+)$/gm,
                            "<h2>$1</h2>"
                        );


                    safeText =
                        safeText.replace(
                            /\*\*(.+?)\*\*/g,
                            "<strong>$1</strong>"
                        );


                    safeText =
                        safeText.replace(
                            /^- (.+)$/gm,
                            "• $1"
                        );


                    safeText =
                        safeText.replace(
                            /^\\\* (.+)$/gm,
                            "• $1"
                        );


                    safeText =
                        safeText.replace(
                            /\n/g,
                            "<br>"
                        );


                    return `
                        <section class="report-section">
                            ${safeText}
                        </section>
                    `;
                }
            )
            .join("");
}


/* ==========================================================
   SOURCES
========================================================== */

function renderSources(
    sources = []
) {

    if (sourceTotal) {

        sourceTotal.textContent =
            sources.length;
    }


    if (topSourcesList) {

        if (!sources.length) {

            topSourcesList.innerHTML =
                "<li>No sources available.</li>";

        } else {

            topSourcesList.innerHTML =
                sources
                    .slice(0, 5)
                    .map(
                        (source) => `

                            <li class="top-source">

                                <strong>
                                    ${escapeHTML(
                                        source.title ||
                                        "Source"
                                    )}
                                </strong>

                                <span>
                                    ${escapeHTML(
                                        source.url ||
                                        ""
                                    )}
                                </span>

                            </li>

                        `
                    )
                    .join("");
        }
    }


    if (allSources) {

        if (!sources.length) {

            allSources.innerHTML = `
                <p class="empty-state">
                    No sources available.
                </p>
            `;

        } else {

            allSources.innerHTML =
                sources
                    .map(
                        (source) => `

                            <article class="report-source">

                                <a
                                    href="${escapeHTML(
                                        source.url ||
                                        "#"
                                    )}"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    ${escapeHTML(
                                        source.title ||
                                        "Source"
                                    )}
                                </a>

                                <p>
                                    ${escapeHTML(
                                        source.url ||
                                        ""
                                    )}
                                </p>

                            </article>

                        `
                    )
                    .join("");
        }
    }
}


/* ==========================================================
   AI REVIEW
========================================================== */

function renderReview(
    review = {}
) {

    if (!reviewContent) {

        return;
    }


    const criticStatus =
        review.status ||
        "—";


    const criticFeedback =
        review.feedback ||
        "No critic feedback available.";


    if (reviewScore) {

        reviewScore.textContent =
            criticStatus;
    }


    let statusClass = "";


    if (
        criticStatus ===
        "PASS"
    ) {

        statusClass =
            "review-pass";

    } else if (
        criticStatus ===
        "NEEDS IMPROVEMENT"
    ) {

        statusClass =
            "review-needs-improvement";
    }


    reviewContent.innerHTML = `

        <div class="review-box">

            <div class="review-status ${statusClass}">

                ${escapeHTML(
                    criticStatus
                )}

            </div>


            <div class="review-feedback">

                <h4>
                    Critic Feedback
                </h4>

                <p>
                    ${escapeHTML(
                        criticFeedback
                    )}
                </p>

            </div>

        </div>
    `;
}


/* ==========================================================
   SUMMARY
========================================================== */

function renderSummary(
    summary = ""
) {

    if (!summaryContent) {

        return;
    }


    summaryContent.innerHTML = `

        <div class="summary-box">

            <p>
                ${escapeHTML(
                    summary ||
                    "No summary available."
                )}
            </p>

        </div>
    `;
}


/* ==========================================================
   REPORT TABS
========================================================== */

function setupTabs() {

    const tabs =
        document.querySelectorAll(
            ".report-tab"
        );


    const reportArea =
        document.getElementById(
            "reportContent"
        );


    const panels = {

        sources:
            document.getElementById(
                "sourcesPanel"
            ),

        review:
            document.getElementById(
                "reviewPanel"
            ),

        summary:
            document.getElementById(
                "summaryPanel"
            )
    };


    tabs.forEach(
        (tab) => {

            tab.addEventListener(
                "click",
                () => {

                    const selected =
                        tab.dataset.tab;


                    tabs.forEach(
                        (item) => {

                            item.classList.remove(
                                "active"
                            );
                        }
                    );


                    tab.classList.add(
                        "active"
                    );


                    if (reportArea) {

                        reportArea.classList.toggle(
                            "hidden",
                            selected !== "report"
                        );
                    }


                    Object.entries(
                        panels
                    ).forEach(
                        ([name, panel]) => {

                            if (panel) {

                                panel.classList.toggle(
                                    "hidden",
                                    selected !== name
                                );
                            }
                        }
                    );
                }
            );
        }
    );
}


/* ==========================================================
   REPORT ACTIONS
========================================================== */

function setupActions() {

    const downloadButton =
        document.getElementById(
            "downloadReport"
        );


    const shareButton =
        document.getElementById(
            "shareReport"
        );


    const viewAllSources =
        document.getElementById(
            "viewAllSources"
        );


    if (viewAllSources) {

        viewAllSources.addEventListener(
            "click",
            () => {

                const sourcesTab =
                    document.querySelector(
                        '.report-tab[data-tab="sources"]'
                    );


                if (sourcesTab) {

                    sourcesTab.click();
                }
            }
        );
    }


    if (downloadButton) {

        downloadButton.addEventListener(
            "click",
            () => {

                alert(
                    "PDF export will be connected to Django."
                );
            }
        );
    }


    if (shareButton) {

        shareButton.addEventListener(
            "click",
            async () => {

                const shareData = {

                    title:
                        reportTitle?.textContent ||
                        "ResearchAI Report",

                    text:
                        "Research report generated by ResearchAI.",

                    url:
                        window.location.href
                };


                if (
                    navigator.share
                ) {

                    try {

                        await navigator.share(
                            shareData
                        );

                    } catch {

                        /*
                            User cancelled sharing.
                        */
                    }

                } else {

                    try {

                        await navigator.clipboard.writeText(
                            window.location.href
                        );


                        shareButton.textContent =
                            "✓ Link copied";


                        setTimeout(
                            () => {

                                shareButton.textContent =
                                    "⤴ Share";

                            },
                            1800
                        );

                    } catch {

                        alert(
                            "Unable to copy the report link."
                        );
                    }
                }
            }
        );
    }
}


/* ==========================================================
   LOAD REPORT FROM DJANGO
========================================================== */

async function loadReport() {

    if (!reportResearchId) {

        if (reportContent) {

            reportContent.innerHTML = `
                <p class="empty-state">
                    No research report was found.
                </p>
            `;
        }

        return;
    }


    try {

        console.log(
            "Loading research report:",
            reportResearchId
        );


        const response =
            await fetch(
                `${API_BASE_URL}/api/research/${encodeURIComponent(
                    reportResearchId
                )}/`
            );


        if (!response.ok) {

            throw new Error(
                `Report request failed: ${response.status}`
            );
        }


        const data =
            await response.json();


        console.log(
            "Report API response:",
            data
        );


        /* ==================================================
           TITLE
        ================================================== */

        if (reportTitle) {

            reportTitle.textContent =
                data.question ||
                "Research Report";
        }


        /* ==================================================
           DATE
        ================================================== */

        if (reportDate) {

            reportDate.textContent =
                data.created_at ||
                "ResearchAI";
        }


        /* ==================================================
           FINAL REPORT
        ================================================== */

        renderReport(
            data.final_report || ""
        );


        /* ==================================================
           CRITIC REVIEW
        ================================================== */

        renderReview({

            status:
                data.critic_status || "",

            feedback:
                data.critic_feedback || ""

        });


        /* ==================================================
           WORD COUNT
        ================================================== */

        if (wordTotal) {

            const calculatedWords =
                String(
                    data.final_report || ""
                )
                    .trim()
                    .split(/\s+/)
                    .filter(Boolean)
                    .length;


            wordTotal.textContent =
                calculatedWords.toLocaleString();
        }


        /* ==================================================
           SOURCES
        ================================================== */

        renderSources(
            data.sources || []
        );


        /* ==================================================
           SUMMARY
        ================================================== */

        renderSummary(
            data.summary || ""
        );


        /* ==================================================
           SOURCE RELIABILITY
        ================================================== */

        if (sourceReliability) {

            sourceReliability.textContent =
                calculateSourceReliability(
                    data.sources || []
                );
        }


        /* ==================================================
           GOOGLE ANALYTICS
           REPORT VIEWED EVENT
        ================================================== */

        /*
            The report was successfully loaded
            from the Django API.

            Therefore, record that the user
            viewed a research report.
        */

        if (
            typeof gtag === "function"
        ) {

            gtag(
                "event",
                "report_viewed"
            );


            console.log(
                "Google Analytics event sent: report_viewed"
            );

        } else {

            console.warn(
                "Google Analytics gtag function is not available."
            );
        }

    }

    catch (error) {

        console.error(
            "REPORT ERROR:",
            error
        );


        if (reportContent) {

            reportContent.innerHTML = `
                <p class="empty-state">
                    Unable to load the report.
                    Make sure the Django API is running.
                </p>
            `;
        }
    }
}


/* ==========================================================
   INITIALIZE
========================================================== */

setupTabs();

setupActions();

loadReport();