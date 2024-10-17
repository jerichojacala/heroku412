#mini_fb/models.py
#Define the data objects for our application
#Jericho Jacala jjacala@bu.edu

from django.db import models

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the idea of one profile'''

    #data attributes of an article:
    firstname = models.TextField(blank=False)
    lastname = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this object'''
        return f'{self.firstname} {self.lastname}'
    
    def get_status_messages(self):
        '''Return a QuerySet of all StatusMessages on this Profile'''

        #use the ORM to retrieve Comments for which the FK is this Article
        status_messages = StatusMessage.objects.filter(profile=self)
        return status_messages
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now=True) #fields for StatusMessage
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    
    def __str__(self):
        '''Return a string representation of this object'''
        return f'{self.message}'
    
    def get_images(self):
        '''Return a QuerySet of all Images on this StatusMessage'''
        #use the ORM to retrieve Images for which the FK is this StatusMessage
        images = Image.objects.filter(statusmessage=self)
        return images

    
class Image(models.Model):
    statusmessage = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    imagefile = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this object'''
        return f'{self.timestamp}'
