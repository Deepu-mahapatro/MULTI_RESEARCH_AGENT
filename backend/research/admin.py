from django.contrib import admin

from .models import Research


# Register the Research model with Django Admin.
#
# This allows us to view and manage Research records
# through Django's built-in admin panel.
@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):

    # These fields will be displayed as columns
    # in the Django Admin research list.
    list_display = [
        "id",
        "question",
        "status",
        "created_at",
        "updated_at",
    ]

    # Allows us to search research records
    # using the question field.
    search_fields = [
        "question",
    ]

    # Allows us to filter records by their status.
    list_filter = [
        "status",
    ]