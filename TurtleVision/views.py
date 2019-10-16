from django.shortcuts import render, get_object_or_404
from django.views import View
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from .models import Session, Movie, Frame
from django.views.generic.edit import FormView
from .forms import VideoForm
from .datamanage import CSVdump

#access the TurtleVision welcome page--index
#this is the welcome page for the Turtle Vision application. It will provide some dynamic information
#as well as a breif discription of how the project operates

class index(View):
     def get(self,request):
          num_sessions = Session.objects.all().count()
          num_movies = Movie.objects.all().count()
          num_frames = Frame.objects.all().count()

          context = {
               'num_sessions':num_sessions,
               'num_movies':num_movies,
               'num_frames':num_frames,
          }

          return render(request, 'index.html', context=context)







#TO-DO: create upload class.
#The upload view will have a form which will let a user upload a series of (very large) videos
#In addition to blank csv logs
#This will create a new instance of the "session" model, several new "movie" instances, and a shit ton of seconds

#Before deploying: understand security risk of using forms

class upload(FormView):
     form_class = VideoForm
     template_name = 'upload.html'
     success_url = 'success/'
    
     # Form for uploading files: http://www.learningaboutelectronics.com/Articles/How-to-create-a-video-uploader-with-Python-in-Django.php
     # File to secondDat instances: use csv delimiter https://realpython.com/python-csv/
     def post(self,request,*args,**kwargs):
          form_class = self.get_form_class()
          form = self.get_form(form_class)
          vid_files = request.FILES.getlist('video_file_field')
          current_ses = Session(record_date = request.POST.get('session_date'), loc_name = request.POST.get('session_loc'), csv_log = request.FILES['CSV_file_field'])
          current_ses.save()        
          if form.is_valid():
               for f in vid_files:
                    n = str(f)
                    newM = Movie(session = current_ses, name = n, videofile = f)
                    newM.save()
               #This part is not modular. Figure out a new way to create the second instances. For now use dump function
               csvIns = CSVdump(current_ses)
               csvIns.createSeconds()
               return self.form_valid(form)
          else:
               return self.form_invalid(form)
     
def uploadSuccess(request):
     return render(request, 'uploadSuccess.html', {})







#In the train control-panel there will be:
#	1)a select session option -- SKIP FOR ALPHA
#	2)a select movie within session option -- SKIP FOR ALPHA
#	3)a select analysis type section -- SKIP FOR ALPHA
#	4)TO-DO: buttons that achieve goals of particular analysis

class train(View):
     def get(self,request,*arg,**kwargs):
           sessionChoices = Session.objects.all()
           sessionSelected = kwargs['session_choice']
           try:
                movieChoices = Movie.objects.all().filter(session__pk=sessionSelected.pk)
           except Exception as e:
                movieChoices = ''
           context={
                'session_choices':sessionChoices,
                'movie_choices':movieChoices
           }
           return render(request, 'train.html', context=context)
     def post(self, request, *args, **kwargs):
           kwargs={session_choice
           return HttpResponseRedirect(reverse('train', kwargs))



#main goal:
#	1)a button is pushed on "train" view by human or machine
#	2)saveFrame is called with the button information and the frame
#	3)the frame is stored to the correct folder and a new Frame instance is created

#saveFrame is going to be called from jqueary/ajax
#a paramter will be the type of analysis that is to be booked

#FOR BETA -- the images are going to be saved in their full .png format
#	in late versions we want the images to be "transformed" (currently taking place in "trust" view) before they are stored for optimal space
#	for later versions, the frame information ought to be only stored as a field to a model. It is not necesarry to save as .png files

#this part of the program is inspired by https://lethain.com/two-faced-django-part-5-jquery-ajax/

def saveFrame(request):
     new_frame = Frame.objects.create()
     movieChoice = Movie.objects.get()
     context={
	 'movie_choice':movieChoice
     }
     return render(request, 'train.html', context=context)











#The trust section is password protected and only allows admittance to the admin
#It has information which will explain the process of deep learning
#There will be a button that executes the model training

#TO-DO: Create AImodel in models.py
#FOR BETA -- this is where this will happen:
#https://towardsdatascience.com/a-beginners-tutorial-on-building-an-ai-image-classifier-using-pytorch-6f85cb69cba7

class trust(View):
      def get(self,request):
          return render(request, 'trust.html', {})