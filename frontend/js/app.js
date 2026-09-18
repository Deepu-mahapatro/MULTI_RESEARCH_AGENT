/* ==========================================================
   RESEARCHAI
   GLOBAL APPLICATION JAVASCRIPT
   THEME / LIGHT & DARK MODE
========================================================== */


/* ==========================================================
   GET THEME ELEMENTS
========================================================== */

const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.querySelector(".theme-icon");
const themeLabel = document.querySelector(".theme-label");


/* ==========================================================
   APPLY THEME
========================================================== */

function applyTheme(theme) {

    document.documentElement.setAttribute(
        "data-theme",
        theme
    );


    /* Update button */

    if (theme === "dark") {

        if (themeIcon) {
            themeIcon.textContent = "☾";
        }

        if (themeLabel) {
            themeLabel.textContent = "Dark mode";
        }

    } else {

        if (themeIcon) {
            themeIcon.textContent = "☼";
        }

        if (themeLabel) {
            themeLabel.textContent = "Light mode";
        }
    }
}


/* ==========================================================
   LOAD SAVED THEME
========================================================== */

const savedTheme = localStorage.getItem("researchai-theme");


if (savedTheme === "dark" || savedTheme === "light") {

    applyTheme(savedTheme);

} else {

    /*
       Default theme
       Change this to "dark" if you want dark mode
       as the default.
    */

    applyTheme("light");
}


/* ==========================================================
   THEME TOGGLE
========================================================== */

if (themeToggle) {

    themeToggle.addEventListener("click", function () {

        const currentTheme =
            document.documentElement.getAttribute("data-theme");

        const newTheme =
            currentTheme === "dark"
                ? "light"
                : "dark";


        applyTheme(newTheme);


        /* Save user's choice */

        localStorage.setItem(
            "researchai-theme",
            newTheme
        );

    });

}