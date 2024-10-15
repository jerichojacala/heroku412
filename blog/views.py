#blog/view.py
#dfine the views for the blog app

from django.shortcuts import render
import random

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import * #import the models
from .forms import * #import the forms
from django.urls import reverse
from typing import Any

#class-based view
class ShowAllView(ListView):
    '''the view to show all Articles'''
    model = Article #the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' #this is the context variables to use in the template
    
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