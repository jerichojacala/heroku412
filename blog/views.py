#blog/view.py
#dfine the views for the blog app

from django.shortcuts import render,redirect
import random

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import * #import the models
from .forms import * #import the forms
from django.urls import reverse
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse as HttpResponse
from django.http import HttpRequest

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

#class-based view
class ShowAllView(ListView):
    '''the view to show all Articles'''
    model = Article #the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' #this is the context variables to use in the template

    def dispatch(self, *args, **kwargs):
        '''implement this method to add some debug tracing'''

        print(f"ShowAllView.dispatch; self.request.user={self.request.user}")

        #let the superclass version of this method do its work
        return super().dispatch(*args, **kwargs)
    
class RandomArticleView(DetailView):
    '''Display one Article selected at random'''
    model = Article #the model to display
    template_name = "blog/article.html"
    context_object_name = "article"

    #AttributeError
    #one solution: implement get_object method
    def get_object(self):
        '''Return one Article chosen at random'''

        #retrieve all of the articles
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
    
class ArticleView(DetailView):
    '''Display one Article selected at random'''
    model = Article #the model to display
    template_name = "blog/article.html"
    context_object_name = "article"
    
class CreateCommentView(CreateView):
    '''
    A view to create a Comment on an article
    on GET: send back the form to display
    on POST: read/process the form, and save new Comment to the database
    '''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        #get the context data from the superclass
        context = super().get_context_data(**kwargs)

        #find the Article identified by the PK from the URL pattern
        article = Article.objects.get(pk=self.kwargs['pk'])

        #add the Article referred to by the URL into this context
        context['article'] = article
        return context

    def get_success_url(self) -> str:
        #return 'show_all'
        #article = Article.objects.get(pk=self.kwargs['pk'])
        #return reverse('article',kwargs={'pk':article.pk})
        return reverse('article',kwargs=self.kwargs)

    def form_valid(self,form):
        '''This method is called after the form is validated, before saving data to the database'''

        
        print(f'CreateCommentView.form_valid(): form={form}')
        print(f'CreateCommentView.form_valid(): self.kwargs={self.kwargs}')

        #find the Article identified by the PK from the URL pattern
        article = Article.objects.get(pk=self.kwargs['pk'])

        #attach this Article to the instance of the Comment to set its FK
        form.instance.article = article #like: comment.article = article

        #delegate work to superclass form
        return super().form_valid(form)
    
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view class to create a new Article instance'''
    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')
    def form_valid(self, form):
        '''This method is called as part of the form processing'''
        print(f'CreateArticleView.form_valid(): form.cleaned_data={form.cleaned_data}')

        #find the user who is logged in
        user = self.request.user

        #attach that user as an FK to the new Article instance
        form.instance.user = user

        #let the superclass do the real work
        return super().form_valid(form)
    
class RegistrationView(CreateView):
    '''Handle registration of new Users'''
    template_name = 'blog/register.html'
    form_class = UserCreationForm #built in from django.contrib.auth.forms

    def dispatch(self,request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        '''handle the user creation form submission'''

        if self.request.POST:
            print(f"RegistrationView.dispatch: self.request.POST={self.request.POST}")
            #reconstruct the usercreateform from the POST data
            form = UserCreationForm(self.request.POST)
            if not form.is_valid():
                print(f"form.errors={form.errors}")

                #let CreateView.dispatch handle the problem
                return super().dispatch(request, *args, **kwargs)

            #save the form, which creates a new User
            user = form.save() #this will commit the insert to the database
            print(f"RegistrationView.dispatch: created user {user}")

            #log the user in
            login(self.request,user)
            print(f"RegistrationView.dispatch: {user} is logged in.")

            #note for mini_fb: attach the FK user to the Profile form instance

            #return a response
            return redirect(reverse('show_all'))

        return super().dispatch(request, *args, **kwargs)
