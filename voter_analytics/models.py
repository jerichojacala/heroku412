from django.db import models
from datetime import datetime

#voter_analytics/models.py
#define the models for the voter_analytics app
#Jericho Jacala jjacala@bu.edu

# Create your models here.
class Voter(models.Model):
    '''
    Store/represent the data from one voter at the Newton Election.
    Last Name
*    First Name
*    Residential Address - Street Number
*    Residential Address - Street Name
*    Residential Address - Apartment Number
*    Residential Address - Zip Code
*    Date of Birth
*    Date of Registration
*    Party Affiliation
*    Precinct Number
*    v20state
*    v21town
*    v21primary
*    v22general
*    v23town
    '''
    # identification
    vid = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField(null=True,blank=True)
    zip_code = models.IntegerField()
    dob = models.DateField()

    #voter info
    dor = models.DateField()
    party = models.CharField(max_length=3)
    precinct = models.TextField()

    #voter history
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()

    filename = "C:/Users/jerry/Desktop/django - Copy/newton_voters.csv"
    f = open(filename)
    f.readline() # discard headers
    for line in f:
        try:
            fields = [field.strip() for field in line.split(',')]
            # create a new instance of Result object with this record from CSV
            result = Voter(vid=fields[0],
                last_name=fields[1],
                first_name=fields[2],
                street_number = int(fields[3]),
                street_name = fields[4],
                apartment_number=fields[5],
                        
                zip_code = int(fields[6]),
                dob = datetime.strptime(fields[7], "%Y-%m-%d").date(),
                dor = datetime.strptime(fields[8], "%Y-%m-%d").date(),
                party = fields[9],
                precinct = fields[10],
                    
                v20state=fields[11].upper() == "TRUE",
                v21town=fields[12].upper() == "TRUE",
                v21primary=fields[13].upper() == "TRUE",
                v22general=fields[14].upper() == "TRUE",
                v23town=fields[15].upper() == "TRUE",
                voter_score=int(fields[16]),
            )
            result.save() #save this instance to the database
            print(f'Created result: {result}')
        except:
            print(f"Exception on {fields}")