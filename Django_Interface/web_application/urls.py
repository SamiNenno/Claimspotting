from django.urls import path
from .views import *

urlpatterns = [
    path('list_api/', ListDataView.as_view()),
    path('search_api/', SearchDataView.as_view()),
    path('stats_api/', GetStatsView.as_view()),
]