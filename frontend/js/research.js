/* ==========================================================
   RESEARCHAI
   NEW RESEARCH JAVASCRIPT
========================================================== */

"use strict";


/* ==========================================================
   DOM ELEMENTS
========================================================== */

const researchForm =
    document.getElementById(
        "researchForm"
    );

const researchInput =
    document.getElementById(
        "researchTopic"
    );

const errorBox =
    document.getElementById(
        "formError"
    );

const exampleButtons =
    document.querySelectorAll(
        ".example-topic"
    );


/* ==========================================================
   DJANGO API
========================================================== */

const API_BASE_URL = "https://multi-research-agent-luez.onrender.com";


/* ==========================================================
   ERROR HANDLING
========================================================== */

function clearError() {

    if (errorBox) {
        errorBox.textContent = "";
    }
}


function showError(message) {

    if (errorBox) {
        errorBox.textContent = message;
    }
}


/* ==========================================================
   EXAMPLE TOPICS
========================================================== */

exampleButtons.forEach(
    (button) => {

        button.addEventListener(
            "click",
            () => {

                researchInput.value =
                    button.dataset.topic || "";

                researchInput.focus();

                clearError();
            }
        );
    }
);


/* ==========================================================
   RESEARCH FORM
========================================================== */

if (researchForm) {

    researchForm.addEventListener(
        "submit",
        async (event) => {

            /*
                Prevent normal HTML form submission.
            */
            event.preventDefault();


            /*
                Find the submit button inside
                the research form.
            */
            const submitButton =
                researchForm.querySelector(
                    "#startResearchButton"
                );


            clearError();


            /* --------------------------------------------------
               Get research question
            -------------------------------------------------- */

            const question =
                researchInput.value.trim();


            /* --------------------------------------------------
               Validate question
            -------------------------------------------------- */

            if (question.length < 3) {

                showError(
                    "Please enter a research topic."
                );

                researchInput.focus();

                return;
            }


            /* --------------------------------------------------
               Disable submit button
            -------------------------------------------------- */

            if (submitButton) {

                submitButton.disabled = true;

                submitButton.textContent =
                    "Researching…";
            }


            try {

                /* --------------------------------------------------
                   Send request to Django
                -------------------------------------------------- */

                console.log(
                    "Sending research request to Django..."
                );


                const response =
                    await fetch(
                        `${API_BASE_URL}/api/research/`,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({
                                    question: question
                                })
                        }
                    );


                /* --------------------------------------------------
                   Log HTTP status
                -------------------------------------------------- */

                console.log(
                    "Django response status:",
                    response.status
                );


                /* --------------------------------------------------
                   Convert response to JSON
                -------------------------------------------------- */

                const data =
                    await response.json();


                /* --------------------------------------------------
                   Log response
                -------------------------------------------------- */

                console.log(
                    "Django response data:",
                    data
                );


                /* --------------------------------------------------
                   Handle API errors
                -------------------------------------------------- */

                if (!response.ok) {

                    throw new Error(
                        data.details ||
                        data.error ||
                        "Research request failed."
                    );
                }


                /* --------------------------------------------------
                   Check research object
                -------------------------------------------------- */

                if (
                    !data.research ||
                    !data.research.id
                ) {

                    throw new Error(
                        "Research ID was not returned by the API."
                    );
                }


                /* --------------------------------------------------
                   Get research ID
                -------------------------------------------------- */

                const researchId =
                    data.research.id;


                // Track when a user successfully starts a research request.
                if (typeof gtag === "function") {
                   gtag("event", "research_started");
                }


                /* --------------------------------------------------
                   Store current research
                -------------------------------------------------- */

                sessionStorage.setItem(
                    "research_id",
                    String(researchId)
                );

                sessionStorage.setItem(
                    "research_topic",
                    question
                );


                /* --------------------------------------------------
                   Move to progress page
                   
                   IMPORTANT:
                   research.html and progress.html
                   are in the same /pages/ folder.
                -------------------------------------------------- */

                console.log(
                    "Moving to progress page..."
                );


                window.location.href =
                    `progress.html?id=${encodeURIComponent(
                        researchId
                    )}`;
            }


            catch (error) {

                /* --------------------------------------------------
                   Display actual error
                -------------------------------------------------- */

                console.error(
                    "RESEARCH ERROR:",
                    error
                );


                showError(
                    error.message ||
                    "Unable to start research."
                );


                /* --------------------------------------------------
                   Re-enable button safely
                -------------------------------------------------- */

                if (submitButton) {

                    submitButton.disabled =
                        false;

                    submitButton.textContent =
                        "→";
                }
            }
        }
    );
}