## restaurant.urls.py
## define the URLs for this app

from django.urls import path
from django.conf import settings
from . import views

#define a list of valid URL patterns
urlpatterns = [
    path("", views.main, name="main"),
    path("main/",views.main,name="main"), 
    path("order/", views.order, name="order"),
    path("confirmation/",views.confirmation,name="confirmation"),
]
