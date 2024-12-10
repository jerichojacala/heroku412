#project\views.py
#define the views for the app

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from .models import * #import the models
from django.urls import reverse
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin #require some views only be accessed by authenticated users
from django.contrib.auth import login
from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

# Create your views here.
class ShowAllCoursesView(ListView):
    '''the view to show all Courses'''
    model = Course #the model to display
    template_name = 'project/show_all_courses.html' #the template we work with for the view
    context_object_name = 'courses' #this is the context variables to use in the template

    def get_queryset(self):
        '''Returns the queryset of courses based on filters from the search'''

        qs = super().get_queryset() #call superclass to get all courses

        college = self.request.GET.get('college', '').strip() #refine the queryset based on the search input
        subschool = self.request.GET.get('subschool', '').strip() #here we put each criteria in variables
        department = self.request.GET.get('department', '').strip()
        if college: #and here we filter by the criteria if they are not empty- if they are empty they will filter everything!
            qs = qs.filter(college__icontains=college)
        if subschool:
            qs = qs.filter(subschool__icontains=subschool)
        if department:
            qs = qs.filter(department__icontains=department)
    
        return qs
    
class ShowAllProfessorsView(ListView):
    '''the view to show all Professors'''
    model = Professor #the model to display
    template_name = 'project/show_all_professors.html'
    context_object_name = 'professors' #this is the context variables to use in the template

    def get_queryset(self):
        '''Returns the queryset of professors based on filters from the search'''

        qs = super().get_queryset()

        first_name = self.request.GET.get('first_name', '').strip() #refine the queryset based on the search input
        last_name = self.request.GET.get('last_name', '').strip() #store the criteria as variables here
        college = self.request.GET.get('college', '').strip()
        if first_name: #filter by the search criteria where they exist
            qs = qs.filter(first_name__icontains=first_name)
        if last_name:
            qs = qs.filter(last_name__icontains=last_name)
        if college:
            qs = qs.filter(college__icontains=college)
        return qs

class ShowCourseView(DetailView):
    '''Display one Course specified by a primary key'''
    model = Course #the model to display
    template_name = "project/show_course.html"
    context_object_name = "course" #context object we can refer to as a scriptlet
    
    def get_object(self, queryset=None):
        '''get the course we are on from the URL parameters'''
        if 'pk' in self.kwargs: #if we have specified the course we want to go to
            courses = Course.objects.filter(pk=self.kwargs['pk'])
            course = courses.first()#get the first course-band-aid solution if multiple students, but good for our purposes
            return course
        
class ShowProfessorView(DetailView):
    '''Display one Professor specified by a primary key'''
    model = Professor
    template_name = "project/show_professor.html"
    context_object_name = "professor"
    def get_object(self, queryset=None): #get prof that we are logged in as
        if 'pk' in self.kwargs: #if we have specified the prof we want to go to
            professors = Professor.objects.filter(pk=self.kwargs['pk'])
            professor = professors.first()#get the first professor-band-aid solution if multiple students, but good for our purposes
            return professor
        
class ShowStudentView(DetailView):
    '''Display one Student specified by a primary key'''
    model = Student
    template_name = "project/show_student.html"
    context_object_name = "student"
    def get_object(self, queryset=None): #get student that we are logged in as
        if 'pk' in self.kwargs: #if we have specified the student we want to go to
            students = Student.objects.filter(pk=self.kwargs['pk'])
            student = students.first()#get the first student-band-aid solution if multiple students, but good for our purposes
            return student
        else: #otherwise, find the set of students attached to the user we are logged in as and return the first student
            students = Student.objects.filter(user=self.request.user)
            student = students.first()
            return student
        
        
class ShowAllStudentsView(ListView):
    '''the view to show all Student'''
    model = Student #the model to display
    template_name = 'project/show_all_students.html'
    context_object_name = 'students' #this is the context variables to use in the template

    def get_queryset(self):
        '''Returns the queryset of students based on filters from the search'''

        qs = super().get_queryset() #get the queryset of all students

        college = self.request.GET.get('college', '').strip() #refine the queryset based on the search input
        first_name = self.request.GET.get('first_name', '').strip()
        last_name = self.request.GET.get('last_name', '').strip()
        if college: #filter by the various search criteria
            qs = qs.filter(college__icontains=college)
        if first_name:
            qs = qs.filter(first_name__icontains=first_name)
        if last_name:
            qs = qs.filter(last_name__icontains=last_name)
    
        return qs

class CreateReviewView(LoginRequiredMixin,CreateView):
    '''
    A view to create a Review for a Course
    '''

    form_class = CreateReviewForm #the form we associate with the view
    template_name = "project/create_review_form.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Get the context data for use in the template'''
        #get the context data from the superclass
        context = super().get_context_data(**kwargs)

        #find the Courseidentified by the PK from the URL pattern

        course = Course.objects.get(pk=self.kwargs['pk'])

        #add the course from URL parameters into context
        context['course'] = course

        return context
    
    
    def get_success_url(self) -> str:
        '''Redirect to a URL on successful form submission'''
        return reverse('show_course_page',kwargs=self.kwargs) #on successful form submission, redirect to show_course_page

    def form_valid(self,form):
        '''This method is called after the form is validated, before saving data to the database'''

        #find the Course identified by the PK from the URL pattern
        course = Course.objects.get(pk=self.kwargs['pk'])

        #attach this Course to the instance of the review to set its FK
        form.instance.course = course #like: review.course = course

        students = Student.objects.filter(user=self.request.user)
        student = students.first() #filter through all students that have the user we are logged in as, and return the first- if we have more than one student for user then some will be inaccessible, but we never intend this to be the case

        form.instance.student = student

        if (Review.objects.filter(student=form.instance.student, course=form.instance.course).exists()): #check if a review has been added- we do not want review spamming!
            return super().form_invalid(form)

        #attach this Student to the instance of the Review to set its FK
        form.instance.student = student #like: review.student = student

        #delegate work to superclass form
        return super().form_valid(form)
        
class DeleteReviewView(LoginRequiredMixin,DeleteView):
    '''Delete a given Review'''
    model = Review #the model to work with
    template_name = 'project/delete_review.html' #the template
    context_object_name = 'review'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Get the course field to find its primary key'''
        # Get the context data from the superclass
        context = super().get_context_data(**kwargs)

        # Get the Review object to find the associated course
        review = self.get_object()
        course = review.course

        # Add the Course referred to by the URL into this context
        context['course'] = course
        return context

    def get_success_url(self) -> str:
        '''Redirect to a URL on successful form submission'''
         # Get the course related to the review
        course = self.get_object().course
        return reverse('show_course_page', kwargs={'pk': course.pk})
    
class CreateScheduleView(LoginRequiredMixin,CreateView):
    '''
    A view to create a Schedule for a Student
    '''

    form_class = CreateScheduleForm
    template_name = "project/create_schedule_form.html"
    model = Schedule

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Get the student field to find its primary key'''
        # Get the context data from the superclass
        context = super().get_context_data(**kwargs)

        students = Student.objects.filter(user=self.request.user)
        student = students.first() #find the first Student associated with the user- again, this works for our goals
        context['student'] = student
        return context

    def get_success_url(self) -> str:
        '''Redirect to a URL on successful form submission'''
        # Get the student related to the schedule
        student = self.kwargs.get('pk')
        return reverse('show_student_page', kwargs={'pk': student}) #return to the student page on success
    
    def form_valid(self,form):
        '''This method is called after the form is validated, before saving data to the database'''

        students = Student.objects.filter(user=self.request.user)
        student = students.first()


        #attach this Student to the instance of the Schedule to set its FK
        form.instance.student = student #like: schedule.student = student

        #delegate work to superclass form
        return super().form_valid(form)

class ShowRegistrationsView(LoginRequiredMixin,ListView):
    '''view to show the search results to add a course to a schedule'''
    model = Course #the model to display
    template_name = "project/course_suggestions.html"
    context_object_name = "courses"

    def get_object(self, queryset=None): #get the schedule from the URL parameters so we know what to add the course to
        if 'pk' in self.kwargs:
            schedules = Schedule.objects.filter(pk=self.kwargs['pk'])
            schedule = schedules.first()
            return schedule
        
    def get_queryset(self):
        '''Returns the queryset of courses based on filters from the search'''

        qs = super().get_queryset()
        
        college = self.request.GET.get('college', '').strip() #refine the queryset based on the search input and strip any leading spaces
        subschool = self.request.GET.get('subschool', '').strip()
        department = self.request.GET.get('department', '').strip()
        if college: #filter based on search criteria, ignoring capitalization and checking if the attribute contains the criteria, if nothing in the criteria, don't filter
            qs = qs.filter(college__icontains=college)
        if subschool:
            qs = qs.filter(subschool__icontains=subschool)
        if department:
            qs = qs.filter(department__icontains=department)
    
        return qs
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Get the course field to find its primary key'''
        # Get the context data from the superclass
        context = super().get_context_data(**kwargs)

        # Get the Schedule object from URL parameters
        schedule = Schedule.objects.get(pk=self.kwargs['pk'])

        # Add the schedule referred to by the URL into this context
        context['schedule'] = schedule
        return context

class CreateRegistrationView(LoginRequiredMixin,View):
    '''view to add a Registration to the profile once we have selected a course to add'''
    def dispatch(self, request, *args, **kwargs):
        '''function to add a course'''
        #find the schedule identified by the PK from the URL pattern
        schedule = self.get_object()
        course = Course.objects.get(pk=self.kwargs['other_pk']) #find the course from the other PK specified in the URL

        schedule.add_registration(course) #add the course to the schedule

        return redirect('show_student_page', pk=schedule.student.pk) #return to the page of the student who owns the schedule
    
    def get_object(self, queryset=None): #get schedule from the URL parameters
        if 'pk' in self.kwargs:
            schedules = Schedule.objects.filter(pk=self.kwargs['pk'])
            schedule = schedules.first()
            return schedule

    
class DeleteRegistrationView(LoginRequiredMixin,DeleteView):
    '''Delete a given Registration'''
    model = Registration
    template_name = 'project/delete_registration.html'
    context_object_name = 'registration'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Get the course field to find its primary key'''
        # Get the context data from the superclass
        context = super().get_context_data(**kwargs)

        # Get the Review object to find the associated schedule
        registration = self.get_object()
        schedule = registration.schedule

        # Add the Schedule referred to by the URL into this context
        context['schedule'] = schedule
        return context

    def get_success_url(self) -> str:
        '''Redirect to a URL on successful form submission'''
         # Get the student related to the schedule related to the registration
        schedule = self.get_object().schedule
        return reverse('show_student_page', kwargs={'pk': schedule.student.pk}) #return to the page of the student of the schedule the course is registered to
    
class CreateStudentView(CreateView):
    '''The view to create a Student'''
    form_class = CreateStudentForm #the form we must create
    template_name = "project/create_student_form.html"
    model = Student

    def get_success_url(self) -> str:
        student = self.object #create student as a context variable
        return reverse('show_student_page', kwargs={'pk':student.pk}) #go to show_student_page of the student we created

    def get_login_url(self) -> str:
        '''return the URL of the login page'''
        return reverse('login')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Get the context data for use in the template'''
        #get the context data from the superclass
        context = super().get_context_data(**kwargs)


        context['user_creation_form'] = UserCreationForm(self.request.POST) #put the user creation form in the context so we can attach the user to the Student later
        return context
    
    def form_valid(self,form):
        '''This method is called after the form is validated, before saving data to the database'''
        if self.request.POST:
            userform = UserCreationForm(self.request.POST) #reconstruct UserCreationForm from POST data
            if userform.is_valid(): #if the form is valid
                user = userform.save() #save and login the user, and attach the user to the Student instance
                login(self.request,user)
                form.instance.user = user #attach user to the instance
                form.instance.save() #save the instance to the database
            else:
                return self.form_invalid(form) #otherwise, handle the form being invalid

        #delegate work to superclass form
        return super().form_valid(form)
    
class UpdateStudentView(LoginRequiredMixin,UpdateView):
    '''update a given Student'''
    model = Student
    form_class = UpdateStudentForm
    template_name = 'project/update_student_form.html'
    def get_success_url(self) -> str:
        return reverse('show_student_page',kwargs=self.kwargs) #on successful form submission, redirect to show_student_page
    
    def get_object(self, queryset=None): #get student that we are logged in as
        students = Student.objects.filter(user=self.request.user)
        student = students.first() #get the first student in case there are many-it's a band-aid but good enough for our purposes
        return student
        
class DeleteScheduleView(LoginRequiredMixin,DeleteView):
    '''Delete a given Schedule'''
    model = Schedule
    template_name = 'project/delete_schedule.html'
    context_object_name = 'schedule'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Get the student field to find its primary key'''
        # Get the context data from the superclass
        context = super().get_context_data(**kwargs)

        # Get the Schedule object to find the associated Student
        schedule = self.get_object()
        student = schedule.student #get the student from the schedule and store it in a variable

        # Add the Student referred to by get_object into this context
        context['student'] = student
        return context

    def get_success_url(self) -> str:
        '''Redirect to a URL on successful form submission'''
         # Get the student related to the schedule
        student = self.get_object().student
        return reverse('show_student_page', kwargs={'pk': student.pk}) #return to the page of the student
    
class ShowOthersView(DetailView):
    '''view to show other students who have the course in their schedules'''
    model = Course #the model to display
    template_name = "project/show_others.html"
    context_object_name = "course" #context object we refer to as a scriptlet in the template

    def get_object(self, queryset=None): #get the course from the URL parameters so we know which students to look for
        if 'pk' in self.kwargs:
            courses = Course.objects.filter(pk=self.kwargs['pk'])
            course = courses.first()
            return course