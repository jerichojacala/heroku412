## quotes/views.py
## description: write view functions to handle URL requests for the quotes app

from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest, HttpResponse
import time
import random

quotes = ["Yeah, just pain. It was pain everywhere. So we gotta keep on pushing through and being resilient","Losing, I believe... losing is too easy. And I hate easy stuff.","If I ever get Manziel disease, I want all of you to smack me in the head with your microphones."]
images =['https://pbs.twimg.com/media/GFnB2iLb0AA2oNZ.jpg','https://gray-kplc-prod.cdn.arcpublishing.com/resizer/v2/ACMJGI3KG5GTBAOIYHVFLRKABQ.jpg?auth=fca26bac6979a663c4bd4f3bc34b17d49c4a9c3ffbc7a24b84805f93948d273a&width=800&height=450&smart=true','https://sportshub.cbsistatic.com/i/r/2022/09/07/4d28bab6-81d7-4afb-be50-ad15a2f805b1/thumbnail/1200x675/1bbacfd8bd68a154fc42d887a665fdf0/getty-jameis-winston-saints.jpg']

# Create your views here.
# def home(request):
#     '''Handle the main URL for the quotes app.'''

#     response_text = f'''
#     <html>
#     <h1>Hello, world!</h1>
#     <p>This is our first django web application!</p>
#     <hr>
#     This page was generated at {time.ctime()}.
#     </html>
#     '''
#     # create and return a response to the client:
#     return HttpResponse(response_text)

#def home(request):
#    '''
#    Function to handle the URL request for /quotes (home page).
#    Delegate rendering to the template quotes/home.html.
#    '''
#    # use this template to render the response
#    template_name = 'quotes/home.html'

    # create a dictionary of context variables for the template:
#    context = {
#        "current_time" : time.ctime(),
#        "letter1" : chr(random.randint(65,90)), # a letter from A ... Z
#        "letter2" : chr(random.randint(65,90)), # a letter from A ... Z
#        "number" : random.randint(1,10), # number frmo 1 to 10
#    }

    # delegate rendering work to the template
#    return render(request, template_name, context)

def home1(request):
    '''
#    Function to handle the URL request for /quotes (home page).
#    Delegate rendering to the template quotes/home.html.
#    '''
    template_name = 'quotes/home.html'
    context = {
        "quote" : quotes[random.randint(0,len(quotes)-1)],
        #"image" : images[random.randint(0,len(images)-1)],
        "image" : images[2],
    }
    return render(request, template_name,context)

def quote(request):
    '''
#    Function to handle the URL request for /quote.
#    Delegate rendering to the template quotes/quote.html.
#    '''
    template_name = 'quotes/quote.html'
    #create a dictionary of context variables to select a random quote and image
    context = {
        "quote" : quotes[random.randint(0,len(quotes)-1)],
        #"image" : images[random.randint(0,len(images)-1)],
        "image" : images[2],
    }
    return render(request, template_name,context)

def show_all(request):
    '''
#    Function to handle the URL request for /show_all.
#    Delegate rendering to the template quotes/show_all.html.
#    '''
    template_name = 'quotes/show_all.html'
    imgquote = [
        {
            "quote" : quotes[0],
            "image" : images[0],
        },
        {
            "quote" : quotes[1],
            "image" : images[1],
        },
        {
            "quote" : quotes[2],
            "image" : images[2],
        },
    ]
    context = {
        "imgquote" : imgquote
    }
    return render(request, template_name, context)

def about(request):
    '''
#    Function to handle the URL request for /about.
#    Delegate rendering to the template quotes/about.html.
#    '''
    template_name = 'quotes/about.html'
    context = {
        "quote" : quotes[random.randint(0,len(quotes)-1)],
        #"image" : images[random.randint(0,len(images)-1)],
        "image" : images[2],
    }
    return render(request, template_name, context)