from django.shortcuts import render
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio

# Create your views here.
# voter_analytics/views.py
#define the views for the voter_analyltics app
#Jericho Jacala jjacala@bu.edu

from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
import plotly
import plotly.graph_objects as go

class VotersListView(ListView):
    '''View to display voters'''
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100
    def get_queryset(self):
        
        # default queryset is of all records
        qs = super().get_queryset()

        #handle search form/URL parameters:
        party = self.request.GET.get('party')
        voter_score = self.request.GET.get('voter_score')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        if party:
            qs = qs.filter(party__icontains=party)
        if voter_score:
            qs = qs.filter(voter_score=voter_score)
        if min_dob:
            min_dob = f"{min_dob}-01-01"
            qs = qs.filter(dob__gte=min_dob)
        if max_dob:
            max_dob = f"{max_dob}-01-01"
            qs = qs.filter(dob__lte=max_dob)
        if v20state:
            qs = qs.filter(v20state=True)
        if v21town:
            qs = qs.filter(v21town=True)
        if v21primary:
            qs = qs.filter(v21primary=True)
        if v22general:
            qs = qs.filter(v22general=True)
        if v23town:
            qs = qs.filter(v23town=True)

        return qs
    
    def get_context_data(self, **kwargs):
        '''Get the context data for the app'''
        context = super().get_context_data(**kwargs)
        # preserve GET parameters in context
        context['party'] = self.request.GET.get('party')
        context['voter_score'] = self.request.GET.get('voter_score')
        context['min_dob'] = self.request.GET.get('min_dob')
        context['max_dob'] = self.request.GET.get('max_dob')

        context['v20state'] = self.request.GET.get('v20state')
        context['v21town'] = self.request.GET.get('v21town')
        context['v21primary'] = self.request.GET.get('v21primary')
        context['v22general'] = self.request.GET.get('v22general')
        context['v23town'] = self.request.GET.get('v23town')

        # generate a list of years, for example from 1900 to the current year
        current_year = datetime.now().year
        context['birth_years'] = range(1900, current_year + 1)
        return context

class VoterDetailView(DetailView):
    '''Display a single Result on its own page'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = "r"

class GraphView(ListView):
    '''View to display voters'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_queryset(self):
        '''Get the queryset so we can properly filter the data'''
        # default queryset is of all records
        qs = super().get_queryset()

        #handle search form/URL parameters:
        party = self.request.GET.get('party')
        voter_score = self.request.GET.get('voter_score')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        if party:
            qs = qs.filter(party__icontains=party)
        if voter_score:
            qs = qs.filter(voter_score=voter_score)
        if min_dob:
            min_dob = f"{min_dob}-01-01"
            qs = qs.filter(dob__gte=min_dob)
        if max_dob:
            max_dob = f"{max_dob}-01-01"
            qs = qs.filter(dob__lte=max_dob)
        if v20state:
            qs = qs.filter(v20state=True)
        if v21town:
            qs = qs.filter(v21town=True)
        if v21primary:
            qs = qs.filter(v21primary=True)
        if v22general:
            qs = qs.filter(v22general=True)
        if v23town:
            qs = qs.filter(v23town=True)

        return qs
    
    def get_context_data(self, **kwargs):
        '''Get the context data for the app and generate graphs'''
        context = super().get_context_data(**kwargs)

        context['party'] = self.request.GET.get('party')
        context['voter_score'] = self.request.GET.get('voter_score')
        context['min_dob'] = self.request.GET.get('min_dob')
        context['max_dob'] = self.request.GET.get('max_dob')

        context['v20state'] = self.request.GET.get('v20state')
        context['v21town'] = self.request.GET.get('v21town')
        context['v21primary'] = self.request.GET.get('v21primary')
        context['v22general'] = self.request.GET.get('v22general')
        context['v23town'] = self.request.GET.get('v23town')

        current_year = datetime.now().year
        context['birth_years'] = range(1900, current_year + 1)
        
        #get date of birth values from the queryset
        queryset = self.get_queryset().values_list('dob', flat=True)
        
        #convert dob to datetime and extract the year
        birth_years = pd.to_datetime(queryset, errors='coerce').year.dropna()
        
        #generate the histogram using plotly.express (px)
        fig = px.histogram(birth_years, x=birth_years, nbins=20, title="Distribution of Voter Birth Years")
        fig.update_layout(xaxis_title="Birth Year", yaxis_title="Count of Voters")
        
        #convert the plotly figure to HTML
        histogram_html = pio.to_html(fig, full_html=False)

        #pass the histogram HTML to the context
        context['hist_div'] = histogram_html

        #get party values from the queryset
        queryset = self.get_queryset().values_list('party', flat=True)
        
        #create a dataframe to count the number of voters by party
        party_counts = pd.Series(queryset).value_counts().reset_index()
        party_counts.columns = ['party', 'count']
        
        #generate the pie chart using plotly.express (px)
        fig = px.pie(party_counts, names='party', values='count', title="Voter Distribution by Party")
        
        #convert the plotly figure to HTML
        pie_chart_html = pio.to_html(fig, full_html=False)

        #pass the pie chart HTML to the context
        context['pie_div'] = pie_chart_html

        queryset = self.get_queryset().values_list('v20state','v21town','v21primary', 'v22general', 'v23town')
        
        #convert to a DataFrame for easier manipulation
        elections_df = pd.DataFrame(queryset, columns=['v20state','v21town','v21primary', 'v22general', 'v23town'])

        #count how many voters participated in each election
        participation_counts = elections_df.sum()

        #create a bar chart with the election participation counts
        fig = px.bar(participation_counts, x=participation_counts.index, y=participation_counts.values,
                     labels={'x': 'Election', 'y': 'Number of Voters'},
                     title="Voter Participation in Each Election")

        #convert the plotly figure to HTML
        bar_chart_html = pio.to_html(fig, full_html=False)

        #pass the bar chart HTML to the context
        context['bar_div'] = bar_chart_html

        return context
    
        