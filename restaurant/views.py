## restaurant/views.py
## description: write view functions to handle URL requests for the quotes app

from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpRequest, HttpResponse
import time
import random

specials = ["Blueberry Cupcakes: $1", "Strawberry Donuts: $0.50", "Brown Sugar Thai Tea: $3"]
special_values = ["blueberrycupcake", "strawberrydonut", "brownsugarthaitea"]


#def home(request):

#    Function to handle the URL request for /quotes (home page).
#    Delegate rendering to the template restaurant/main.html.
#    '''
#    template_name = 'restaurant/main.html'
#    context = {
        
#    }
#    return render(request, template_name,context)

def main(request):
    '''
#    Function to handle the URL request for /quotes (home page).
#    Delegate rendering to the template restaurant/main.html.
#    '''
    template_name = 'restaurant/main.html'
    context = {

    }
    return render(request, template_name,context)

def order(request):
    '''
    Show the contact form.
    Delegate rendering to the template restaurant/order.html
    '''

    template_name = "restaurant/order.html"
    item = random.randint(0,len(specials)-1)
    
    context = {
        "special_desc" : specials[item],
        "special_value" : special_values[item],
    }


    return render(request,template_name,context)

def confirmation(request):
    '''
    Handle the form submission.
    Read the form data from the request
    and send it back to a template.
    Delegate rendering to restaurant/confirmation.html
    '''
    template_name = "restaurant/confirmation.html"
    if request.POST:
        # Get form data
        sum = 0
        items = [] #create a list and add checked items to this list, keep a sum variable to keep track of prices
        if request.POST.get('itemdonut'):
            items.append('Single donut: $1')
            sum += 1.00
        if request.POST.get('itemdonutdozen'):
            items.append('Dozen donuts: $10')
            sum += 10.00
        if request.POST.get('itemcupcake'):
            items.append('Cupcake: $1.50')
            sum += 1.50
        if request.POST.get('itemthaitea'):
            items.append('Thai Tea: $5')
            sum += 5.00
        if request.POST.get('itemspecial')=='blueberrycupcake':
            items.append('Blueberry Cupcake: $1')
            sum += 1
        elif request.POST.get('itemspecial')=='strawberrydonut':
            items.append('Strawberry Donut: $0.50')
            sum += 0.50
        elif request.POST.get('itemspecial')=='brownsugarthaitea':
            items.append('Brown Sugar Thai Tea: $3')
            sum += 3.00
        sumstring = f"{sum:.2f}"
        instructions = request.POST['instructions']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        context = {
            'name' : name,
            'items' : items,
            'phone' : phone,
            'email' : email,
            'instructions' : instructions,
            'sumstring' : sumstring,
        }
   
    
    return render(request, template_name,context)
    
    #handle GET request on this URL
    #"ok" solution
    #return HttpResponse("Nope.")

    # a "better" solution
    #return render(request, template_name)

    #an even better yet solution: redirect to the correct URL
        #return redirect("show_form")