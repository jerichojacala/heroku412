#mini_fb/views.py
#define the views for the blog app
#Jericho Jacala jjacala@bu.edu

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import * #import the models
from .forms import *
from django.urls import reverse
from typing import Any

#class-based view
class ShowAllProfilesView(ListView):
    '''the view to show all Profiles'''
    model = Profile #the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' #this is the context variables to use in the template
    
class ShowProfilePageView(DetailView):
    '''Display one Profile specified by a primary key'''
    model = Profile #the model to display
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

class CreateProfileView(CreateView):
    form_class = CreateProfileForm #the form we must create
    template_name = "mini_fb/create_profile_form.html"

    def get_success_url(self) -> str:
        profile = self.object #create profile as a context variable
        return reverse('show_profile_page', kwargs={'pk':profile.pk}) #go to show_profile_page with our parameters
    
class CreateStatusMessageView(CreateView):
    '''
    A view to create a StatusMessage on a Profile
    '''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        #get the context data from the superclass
        context = super().get_context_data(**kwargs)

        #find the Article identified by the PK from the URL pattern
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        #add the Article referred to by the URL into this context
        context['profile'] = profile
        return context
    
    def get_success_url(self) -> str:
        return reverse('show_profile_page',kwargs=self.kwargs) #on successful form submission, reidrect to show_profile_page

    def form_valid(self,form):
        '''This method is called after the form is validated, before saving data to the database'''

        #find the Article identified by the PK from the URL pattern
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        #attach this Profile to the instance of the StatusMessage to set its FK
        form.instance.profile = profile #like: statusmessage.profile = profile

        #delegate work to superclass form
        return super().form_valid(form)