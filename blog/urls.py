## formdata.urls.py
## define the URLs for this app

from django.urls import path
from django.conf import settings
from . import views

#define a list of valid URL patterns
urlpatterns = [
    path(r'',views.RandomArticleView.as_view(),name="random"), ##NEW
    path(r'show_all',views.ShowAllView.as_view(),name="show_all"), #refactor
    path(r'article/<int:pk>',views.ArticleView.as_view(),name="article"), #NEW
    #path(r'create_comment',views.CreateCommentView.as_view(), name="create_comment"),
    path(r'article/<int:pk>/create_comment',views.CreateCommentView.as_view(), name="create_comment"),
    #path(r'about', views.about, name="about"),
]
