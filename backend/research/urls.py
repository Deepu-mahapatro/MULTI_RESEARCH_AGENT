from django.urls import path

from .views import test_api, create_research, get_research


# URLs belonging to the research application.
urlpatterns = [

    # -----------------------------------------------------
    # TEST API
    # -----------------------------------------------------
    # GET /api/test/
    path("test/", test_api),


    # -----------------------------------------------------
    # RESEARCH API
    # -----------------------------------------------------
    # GET  /api/research/
    # POST /api/research/
    path("research/", create_research),


    # -----------------------------------------------------
    # SINGLE RESEARCH API
    # -----------------------------------------------------
    # GET /api/research/<id>/
    #
    # Example:
    # GET /api/research/1/
    path("research/<int:id>/", get_research),
]