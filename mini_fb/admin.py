#mini_fb/admin.py
#tell the admin we want to administer these models
#Jericho Jacala jjacala@bu.edu
from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)