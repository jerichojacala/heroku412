#project/forms.py
#define forms for the app
#Jericho Jacala jjacala@bu.edu

from django import forms
from .models import *

class CreateReviewForm(forms.ModelForm):
    '''A form to add a Review on a Course to the database'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['difficulty'].label = "Weekly Hours Spent"
        self.fields['satisfaction'].label = "Satisfaction (Integer from 0-5)"

    class Meta:
        '''Associate this HTML form with the Review model'''
        model = Review #the model that we are looking to create
        fields = ['difficulty', 'satisfaction', 'grade','semester','year','title','notes'] #the fields we must specify

class CreateScheduleForm(forms.ModelForm):
    '''A form to add a Schedule on a Profile to the database'''
    class Meta:
        '''Associate this HTML form with the Schedule model'''
        model = Schedule
        fields = ['title']

class CreateRegistrationForm(forms.ModelForm):
    '''A form to add a Registration on a Schedule to the database'''
    class Meta:
        '''Associate this HTML form with the Registration model'''
        model = Registration
        fields = ['course']

class CreateStudentForm(forms.ModelForm):
    '''A form to add a Student to the database'''

    def __init__(self, *args, **kwargs):
        '''Override to change some details about how we initialize forms'''
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name" #we don't want the fields to display as "first_name," but as "First Name" for the user
        self.fields['last_name'].label = "Last Name"
    
    class Meta:
        '''Associate this HTML form with the Student model'''
        model = Student #the model we are looking to create
        fields = ['first_name','last_name','email','image_file','college'] #the fields the form must specify

class UpdateStudentForm(forms.ModelForm):
    '''a form to update a Student'''
    class Meta:
        '''Associate with the Student model'''
        model = Student
        fields = ['first_name','last_name','email','image_file','college'] #the fields the form must specify
