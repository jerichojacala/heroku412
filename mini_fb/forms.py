# mini_fb/forms.py
#define forms for the app
#Jericho Jacala jjacala@bu.edu

from django import forms
from .models import Profile, StatusMessage

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a StatusMessage on a Profile to the database'''

    class Meta:
        '''Associate this HTML form with the Comment model'''
        model = StatusMessage #the model that we are looking to create
        fields = ['message'] #the fields we must specify

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database'''

    class Meta:
        '''Associate this HTML form with the Profile model'''
        model = Profile #the model we are looking to create
        fields = ['firstname','lastname','city','email','image_url'] #the fields the form must specify

class UpdateProfileForm(forms.ModelForm):
    '''a form to update a profile'''
    class Meta:
        model = Profile
        fields = ['city','email','image_url'] #the fields the form must specify

class UpdateStatusForm(forms.ModelForm):
    '''a form to update a StatusMessage'''
    class Meta:
        model = StatusMessage
        fields = ['message'] #the fields the form must specify