#voter_analytics/urls.py
#define the urls for the app
#Jericho Jacala jjacala@bu.edu

from django.urls import path
from .views import *

urlpatterns = [
    path('',VotersListView.as_view(), name="voters"),
    path('voters',VotersListView.as_view(), name="voters"),
    path('voter/<int:pk>',VoterDetailView.as_view(), name="detail"),
    path('graphs',GraphView.as_view(), name="graphs"),
]