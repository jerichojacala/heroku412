## formdata.urls.py
## define the URLs for this app

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

#define a list of valid URL patterns
urlpatterns = [
    path(r'',views.RandomArticleView.as_view(),name="random"), ##NEW
    path(r'show_all',views.ShowAllView.as_view(),name="show_all"), #refactor
    path(r'article/<int:pk>',views.ArticleView.as_view(),name="article"), #NEW
    #path(r'create_comment',views.CreateCommentView.as_view(), name="create_comment"),
    path(r'article/<int:pk>/create_comment',views.CreateCommentView.as_view(), name="create_comment"),
    #path(r'about', views.about, name="about"),
    path(r'create_article',views.CreateArticleView.as_view(), name="create_article"),

    #authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name="login1"),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name="logout"),
    path('register/',views.RegistrationView.as_view(), name='register'),
]
