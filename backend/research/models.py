from django.db import models


class Research(models.Model):

    # ---------------------------------------------------------
    # RESEARCH STATUS OPTIONS
    # ---------------------------------------------------------

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("searching", "Searching"),
        ("reading", "Reading"),
        ("writing", "Writing"),
        ("reviewing", "Reviewing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    # ---------------------------------------------------------
    # RESEARCH QUESTION
    # ---------------------------------------------------------

    question = models.TextField()

    # ---------------------------------------------------------
    # CURRENT RESEARCH STATUS
    # ---------------------------------------------------------

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # ---------------------------------------------------------
    # FINAL RESEARCH REPORT
    # ---------------------------------------------------------

    final_report = models.TextField(
        blank=True,
        default=""
    )

    # ---------------------------------------------------------
    # RESEARCH SUMMARY
    # ---------------------------------------------------------
    # Stores a short AI-generated summary of the final report.
    # This will be displayed on the Summary tab.
    # ---------------------------------------------------------

    summary = models.TextField(
        blank=True,
        default=""
    )

    # ---------------------------------------------------------
    # CRITIC FEEDBACK
    # ---------------------------------------------------------

    critic_feedback = models.TextField(
        blank=True,
        default=""
    )

    # ---------------------------------------------------------
    # CRITIC STATUS
    # ---------------------------------------------------------
    # Stores the final decision made by the Critic Agent.
    #
    # Example:
    #
    #     PASS
    #     NEEDS IMPROVEMENT
    #
    # This allows the Report Page to show the actual
    # AI review status.
    # ---------------------------------------------------------

    critic_status = models.CharField(
        max_length=30,
        blank=True,
        default=""
    )

    # ---------------------------------------------------------
    # CREATED TIME
    # ---------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # ---------------------------------------------------------
    # UPDATED TIME
    # ---------------------------------------------------------

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # ---------------------------------------------------------
    # STRING REPRESENTATION
    # ---------------------------------------------------------

    def __str__(self):
        return self.question


# =============================================================
# RESEARCH SOURCE
# =============================================================
#
# One Research can have multiple sources.
#
# Example:
#
# Research
#    ├── GeeksforGeeks
#    ├── Solo.io
#    └── Imperva
#
# These sources will later be displayed on the Report page.
# =============================================================

class ResearchSource(models.Model):

    # ---------------------------------------------------------
    # RELATED RESEARCH
    # ---------------------------------------------------------

    research = models.ForeignKey(
        Research,
        on_delete=models.CASCADE,
        related_name="sources"
    )

    # ---------------------------------------------------------
    # SOURCE TITLE
    # ---------------------------------------------------------

    title = models.CharField(
        max_length=500,
        blank=True,
        default=""
    )

    # ---------------------------------------------------------
    # SOURCE URL
    # ---------------------------------------------------------

    url = models.URLField(
        max_length=2000
    )

    # ---------------------------------------------------------
    # SEARCH RESULT SNIPPET
    # ---------------------------------------------------------

    snippet = models.TextField(
        blank=True,
        default=""
    )

    # ---------------------------------------------------------
    # CREATED TIME
    # ---------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # ---------------------------------------------------------
    # STRING REPRESENTATION
    # ---------------------------------------------------------

    def __str__(self):
        return self.title or self.url