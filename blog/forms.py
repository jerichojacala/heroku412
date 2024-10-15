# blog/forms.py

from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment on an Article to the database'''

    class Meta:
        '''Associate this HTML form with the Comment model'''
        model = Comment
        #fields = ['article','author','text'] #which field sto include in the form
        fields = ['author','text']