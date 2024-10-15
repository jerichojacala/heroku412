## mini_fb/urls.py
## define the URLs for this app

from django.urls import path
from django.conf import settings
from . import views

#define a list of valid URL patterns
urlpatterns = [
    path(r'',views.ShowAllProfilesView.as_view(),name="show_all_profiles"), 
    path(r'profile/<int:pk>',views.ShowProfilePageView.as_view(),name="show_profile_page"), 
    path(r'create_profile',views.CreateProfileView.as_view(),name="create_profile"),
    path(r'<int:pk>/create_status',views.CreateStatusMessageView.as_view(),name="create_status"),  
]