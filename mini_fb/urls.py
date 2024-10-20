## mini_fb/urls.py
## define the URLs for this app
#Jericho Jacala jjacala@bu.edu

from django.urls import path
from django.conf import settings
from . import views

#define a list of valid URL patterns
urlpatterns = [
    path(r'',views.ShowAllProfilesView.as_view(),name="show_all_profiles"), 
    path(r'profile/<int:pk>',views.ShowProfilePageView.as_view(),name="show_profile_page"), 
    path(r'create_profile',views.CreateProfileView.as_view(),name="create_profile"),
    path(r'<int:pk>/create_status',views.CreateStatusMessageView.as_view(),name="create_status"),
    path(r'profile/<int:pk>/update',views.UpdateProfileView.as_view(),name="update_profile"),  
    path(r'status/<int:pk>/delete',views.DeleteStatusMessageView.as_view(),name="delete_status"),
    path(r'status/<int:pk>/update',views.UpdateStatusMessageView.as_view(),name="update_status"),    
]