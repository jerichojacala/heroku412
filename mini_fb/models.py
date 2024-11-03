#mini_fb/models.py
#Define the data objects for our application
#Jericho Jacala jjacala@bu.edu

from django.db import models
from itertools import chain
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the idea of one profile'''

    #data attributes of an article:
    firstname = models.TextField(blank=False)
    lastname = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this object'''
        return f'{self.firstname} {self.lastname}'
    
    def get_status_messages(self):
        '''Return a QuerySet of all StatusMessages on this Profile'''

        #use the ORM to retrieve Comments for which the FK is this Article
        status_messages = StatusMessage.objects.filter(profile=self)
        return status_messages
    
    def add_friend(self, other):
        '''adds a friend to a Profile'''
        if not ((Friend.objects.filter((models.Q(profile1=self) & models.Q(profile2=other)) |(models.Q(profile1=other) & models.Q(profile2=self))).exists()) or self == other): #filter out friends that are already friended or self
            Friend.objects.create(profile1=self,profile2=other) #add friend
    
    def get_friends(self):
        '''Returns the queryset of all friends'''
        querylist = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self)) #create list of friendships that contain self
        friends = []
        for friend in querylist:
            if friend.profile1 == self:
                friends.append(friend.profile2)
            else:
                friends.append(friend.profile1)

        return friends
    
    def get_friend_suggestions(self):
        '''Returns the queryset of profiles as suggested friends'''
        #get all friend IDs related to the current profile
        friends1_ids = Friend.objects.filter(profile1=self).values_list('profile2_id', flat=True)
        friends2_ids = Friend.objects.filter(profile2=self).values_list('profile1_id', flat=True)

        #combine both lists of friend IDs
        friends_ids = set(chain(friends1_ids, friends2_ids))

        #exclude the current profile and existing friends from suggestions
        suggestions = Profile.objects.exclude(id=self.id).exclude(id__in=friends_ids)
        return suggestions
    
    def get_news_feed(self):
        '''Returns the queryset of StatusMessages for the news feed'''
        # Get friends as a QuerySet instead of a list
        friends = Profile.objects.filter(id__in=[friend.id for friend in self.get_friends()])

        # Include the current profile along with friends in one QuerySet
        profiles = friends | Profile.objects.filter(pk=self.pk)
    
        # Filter status messages for both self and friends, ordered by timestamp
        news_feed = StatusMessage.objects.filter(profile__in=profiles).order_by('-timestamp')
    
        return news_feed
    
class StatusMessage(models.Model):
    '''Encapsulate idea of a status message'''
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
    '''encapsulate the idea of an image'''
    statusmessage = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    imagefile = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this object'''
        return f'{self.timestamp}'
    
class Friend(models.Model):
    '''
    Encapsulate friendships between Profiles
    '''
    profile1  = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2  = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    anniversary = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return the string representation of the friendship'''
        return f'{self.profile1} & {self.profile2}'
    
    
        
