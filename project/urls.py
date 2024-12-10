## project/urls.py
## define the URLs for this app
#Jericho Jacala jjacala@bu.edu

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

#define a list of valid URL patterns
urlpatterns = [
    path(r'',views.ShowAllCoursesView.as_view(),name="show_all_courses"),
    path(r'students/',views.ShowAllStudentsView.as_view(),name="show_all_students"),
    path(r'professors/',views.ShowAllProfessorsView.as_view(),name="show_all_professors"),
    path(r'course/<int:pk>',views.ShowCourseView.as_view(),name="show_course_page"),
    path(r'course/<int:pk>/see_others',views.ShowOthersView.as_view(),name="show_others_page"),  
    path(r'professor/<int:pk>',views.ShowProfessorView.as_view(),name="show_professor_page"), 
    path(r'student/',views.ShowStudentView.as_view(),name="show_student_page"),
    path(r'student/<int:pk>',views.ShowStudentView.as_view(),name="show_student_page"),
    path(r'review/course/<int:pk>/create_review',views.CreateReviewView.as_view(),name="create_review"),
    path(r'schedule/student/<int:pk>/create_schedule',views.CreateScheduleView.as_view(),name="create_schedule"),
    path(r'create_student',views.CreateStudentView.as_view(),name="create_student"),
    path(r'student/update',views.UpdateStudentView.as_view(),name="update_student"), 
    path(r'review/<int:pk>/delete',views.DeleteReviewView.as_view(),name="delete_review"),
    path(r'schedule/<int:pk>/delete',views.DeleteScheduleView.as_view(),name="delete_schedule"),
    path(r'registration/<int:pk>/delete',views.DeleteRegistrationView.as_view(),name="delete_registration"),
    path(r'schedule/<int:pk>/add_registration/<int:other_pk>',views.CreateRegistrationView.as_view(),name="add_registration"),
    path(r'schedule/<int:pk>/course_suggestions',views.ShowRegistrationsView.as_view(),name="course_suggestions"),  
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name="logout"), 
]