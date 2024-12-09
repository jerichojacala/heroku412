#project/admin.py
#tell the admin we want to administer these models
#Jericho Jacala jjacala@bu.edu
from django.contrib import admin
from .models import *

# Register your models here.

# Register your models here.
admin.site.register(Student)
admin.site.register(Review)
admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(Schedule)
admin.site.register(Registration)