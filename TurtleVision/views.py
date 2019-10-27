from django.http import HttpResponse, StreamingHttpResponse, JsonResponse

from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views import View

#TO-DO: impliment get_object_or_404 (for first deploy)
from django.shortcuts import render, get_object_or_404

from .models import Session, Movie, SecondDat, tag, tagAssign, Frame, tagType
from .forms import VideoForm
from .datamanage import CSV, FrameCreate, MovieHLSCreate, fillSession
from .dataAnalyze import initiateModel, applyModel

import gc




#TO-DO: update info section to contain more interesting and important information (for first deploy)

#Index class currently displayed as welcome page.
#called from urls-- path:'' name:'index'
#refferences-- "welcome" in generic_base
#imports used-- .models, render
#returns-- rendered html
#function-- none/display

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






#TO-DO: impliment required user admin login to access page (for first deploy)
#TO-DO: impliment loading emplem for upload status (for first deploy)
#TO-DO: impliment red field if no input and form subit attempt (for first deploy)

#upload class is a form for admin users to upload 'Sessions' containing 'Movies' and 'secondDat'
#called from urls-- path:'upload/' name:'upload'
#refferences-- "upload" in generic_base
#imports used-- .forms, .models, FormView, render
#returns-- valid form confirmation to redirect to success page
#function-- 
	#1: displays blank VideoForm via 'upload.html'
	#2: create instance of model: Session based on date and location
	#3: access 'datamanage' API to create Movie and secondDat instances
	# Required input from request -- SessionInfo, Movie list, log.csv with precise format

#inspired by-- http://www.learningaboutelectronics.com/Articles/How-to-create-a-video-uploader-with-Python-in-Django.php https://realpython.com/python-csv/

class upload(FormView):
	form_class = VideoForm
	template_name = 'upload.html'
	success_url = 'success/'
	
	def post(self,request,*args,**kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		vid_files = request.FILES.getlist('video_file_field')

		current_ses = Session(record_date = request.POST.get('session_date'), loc_name = request.POST.get('session_loc'), csv_log = request.FILES['CSV_file_field'])
		current_ses.save()        

		if form.is_valid():
			fStore = MovieHLSCreate(vid_files)
			fStore.storeMovies(current_ses)
              
			csvIns = CSV(current_ses)
			csvIns.createSeconds()
			return self.form_valid(form)
		else:
			return self.form_invalid(form)


#uploadSuccess is called when upload view has processed a new Session with subcategories successfully

def uploadSuccess(request):
	return render(request, 'uploadSuccess.html', {})













#TO-DO: make a user_type which logs who creates tag instances to give more power to admin (for first deploy)
#TO-DO: extend tag_type options (for first deploy)

#train is meant to display uploaded videos for the common user to enjoy and provide frame instances to the deep learning model if they wish
#called from urls-- path:'train/' name:'train'
#refferences-- "train" in generic_base
#imports used-- .models, render
#returns-- html page displaying selector with sessions available and an adaptive selector populated based on session decision
#function-- 
	#1: Display movie 72 by default, populate session options
	#2: Display tag_type analysis selectors
	#3: provide buttons for user to take snap shot of video
	#4: display video snapshot on the sidepanel
	#5: provide save button for user to log frame with specified tag

class train(View):

     def get(self, request):
          session_choices = Session.objects.all()
          movie_choice_pk = 72
          movie_choice = Movie.objects.all().get(pk=movie_choice_pk)
          tag_choices = tagType.objects.all()
          context ={
               'tag_choices':tag_choices,
               'session_choices':session_choices, 
               'movie_choice':movie_choice,
          }
          return render(request, 'train.html', context=context)
    
def get_movies(request):
     print("here")
     session_pk = request.GET.get('session_choice')
     session = Session.objects.get(pk=session_pk)
     movies = Movie.objects.all().filter(session__pk = session_pk)

     return render(request, 'train_seg/movie_list.html', {'movie_choices':movies})


#the django system isn't letting me delete this function. Currently it is not effectlively doing anything
#Consider chunking video load https://stackoverflow.com/questions/8600843/serving-large-files-with-high-loads-in-django
def load_video(request):
     movie_sel = request.GET.get('movie_choice')
     src_file = Movie.objects.all().get(pk=movie_sel)
     return render(request, 'train_seg/load_video.html', {'movie_choice':src_file})




#saveFrame is called by ajax from the 'train' page 
#js grabs the current time of streamed video when a button is clicked on the side-panel
#the button is associated with a 'tag_num' which falls under a 'tag_type'
#ajax sends data through frameGrabber.js: movie_pk, second, tag
#saveFrame takes the information and sends to 'datamanage' API to create an instance of Frame

def saveFrame(request):
     get_tag = request.GET.get('tag')

     get_sec = request.GET.get('sec')
     s1 = float(get_sec)

     get_src_lit = request.GET.get('src')


     f1 = FrameCreate(s1,get_src_lit,get_tag)
     f1.createFrameInstance()

     gc.collect()
     return JsonResponse(get_tag,safe=False)














#TO-DO: understand and develop a deep learning model (for first test)
#TO-DO: given understanding of learning model make occupySecondData functional (for first test)

#TO-DO: impliment required user admin login to access page (for first deploy)
#TO-DO: impliment loading emplem for upload status (for first deploy)
#TO-DO: impliment red field if no input and form subit attempt (for first deploy)

#TO-DO: impliment https://github.com/HHTseng/video-classification (for later updates)

#In early additions, as I gain understanding of GLUON, trust is where all of the data processing will happen

#trust is meant to display options for an administrator to update deep learning models, run a model analysis on a session, and download data on a session
#called from urls-- path:'trust/' name:'trust'
#refferences-- "trust" in generic_base
#returns-- html page displaying selector with sessions available and a selector displayingh the tag_type options
#function-- 
	#1: The administrator is able to create and train a deep learning model so far as they have selected a tag_type
	#2: The administrator is able to analyze a session using the recently created model
	#3: The administrator is able to download a csv demonstrating the data that has been processed


class trust(View):
      def get(self,request):
          session_choices = Session.objects.all()
          alltags = tagType.objects.all()
          context ={
               'tag_choices':alltags,
               'session_choices':session_choices, 
          }
          return render(request, 'trust.html', context)

	
def loadAndTrain(request, **kwargs):
        anal_choice = kwargs['an_type']
        tagCat = tagType.objects.get(pk=anal_choice)
        newM = initiateModel(tagCat)
        train_set = newM.createDataArray()
        newM.defineAndTrainModel(train_set)

        response = HttpResponse("<p>Completed Load</p>")
        return response


def occupySecondDat(request, **kwargs):
	session_choice = kwargs['session_id']
	anal_choice = kwargs['an_type']
	sessionFill = fillSession(session_choice,anal_choice)
	sessionFill.occupySeconds()
	response = HttpResponse("<p>Completed Second Analaysis</p>")
	return response

#adapted from https://studygyaan.com/django/how-to-export-csv-file-with-django

def returnCSV(request, **kwargs):
	session_choice = kwargs['session_id']
	current_ses = SecondDat.objects.filter(session__pk=session_choice).order_by('session_time')

	csvIns = CSV(current_ses)

	return csvIns.secondsToCSV()