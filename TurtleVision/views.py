from django.shortcuts import render, get_object_or_404
from django.views import View
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from .models import Session, Movie, Frame
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .forms import VideoForm
from .datamanage import CSVdump
from django.http import JsonResponse

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

# using https://stackoverflow.com/questions/33531502/how-can-ajax-work-with-a-dynamic-django-dropdown-list for list update function

class train(View):

     def get(self, request,**kwargs):
          session_choices = Session.objects.all()
          movie_choice_pk = kwargs['movie_choice']
          movie_choice = Movie.objects.all().get(pk=movie_choice_pk)
          context ={
               'session_choices':session_choices, 
               'movie_choice':movie_choice,
          }
          return render(request, 'train.html', context=context)
    
def get_movies(request):
     session_pk = request.GET.get('session_choice')
     session = Session.objects.get(pk=session_pk)
     movies = Movie.objects.all().filter(session__pk = session_pk)

     return render(request, 'train_seg/movie_list.html', {'movie_choices':movies})

def load_video(request):
     movie_sel = request.GET.get('movie_choice')
     src_file = Movie.objects.all().get(pk=movie_sel)
     return render(request, 'train_seg/load_video.html', {'movie_choice':src_file})


#main goal:
#	1)a button is pushed on "train" view by human or machine
#	2)saveFrame is called with the button information and the frame
#	3)the frame is stored to the correct folder and a new Frame instance is created

#saveFrame is going to be called from jqueary/ajax
#a paramter will be the type of analysis that is to be booked

#FOR ALPHA -- the images are going to be saved in their full .png format
#	in late versions we want the images to be "transformed" (currently taking place in "trust" view) before they are stored for optimal space
#	for later versions, the frame information ought to be only stored as a field to a model. It is not necesarry to save as .png files

#this part of the program is inspired by https://lethain.com/two-faced-django-part-5-jquery-ajax/

def saveFrame(request):

     png = request.POST.get('image')
     get_tag = request.POST.get('tag')
     new_frame = Frame(pngFile=png, tag=get_tag)
     new_frame.save()

     return JsonResponse()











#The trust section is password protected and only allows admittance to the admin
#It has information which will explain the process of deep learning
#There will be a button that executes the model training

#TO-DO: Create AImodel in models.py
#FOR BETA -- this is where this will happen:
#https://towardsdatascience.com/a-beginners-tutorial-on-building-an-ai-image-classifier-using-pytorch-6f85cb69cba7

class trust(View):
      def get(self,request):
          return render(request, 'trust.html', {})