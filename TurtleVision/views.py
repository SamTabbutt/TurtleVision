from django.http import HttpResponse, StreamingHttpResponse, JsonResponse, HttpResponseRedirect

from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views import View

#TO-DO: impliment get_object_or_404 (for first deploy)
from django.shortcuts import render, get_object_or_404

from .models import Session, Movie, SecondDat, tag, tagAssign, Frame, tagType
from .forms import SessionForm, VideoForm
from .datamanage import CSV, FrameCreate, MovieHLSCreate, fillSession
from .dataAnalyze import initiateModel, applyModel

from django.views.decorators.csrf import csrf_protect, csrf_exempt

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
		
		num_surface = Frame.objects.filter(tag__tag_type__name = "SurfaceTime").count()
		num_breath = Frame.objects.filter(tag__tag_type__name = "BreathStatus").count()
		num_flipper = Frame.objects.filter(tag__tag_type__name = "FlipperBeat").count()
		num_sessions = Session.objects.all().count()
		num_movies = Movie.objects.all().count()
		num_frames = Frame.objects.all().count()

		context = {
			'num_sessions':num_sessions,
			'num_movies':num_movies,
			'num_frames':num_frames,
			'num_breath':num_breath,
			'num_flipper':num_flipper,
			'num_surface':num_surface,
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
#adapted from-- https://simpleisbetterthancomplex.com/tutorial/2016/11/22/django-multiple-file-upload-using-ajax.html

class upload(View):
	def get(self, request):
		session_choices = Session.objects.all()
		return render(self.request, 'upload.html',{'session_choices':session_choices})
	
	def post(self,request,*args,**kwargs):
		session_form = SessionForm(request.POST)       

		if session_form.is_valid():
			current_ses = Session(record_date = request.POST.get('session_date'), loc_name = request.POST.get('session_loc'), turtle_name = request.POST.get('session_turtle'))
			current_ses.save()
			session_choices = Session.objects.all()
			return render(self.request, 'upload.html',{'session_choices':session_choices})
		else:
			return HttpResponse('Nothing Changed')

	#Obviously overkill on the code. For now leave it like this, but eventually deal with all file uploads with same method
	@csrf_exempt
	def videos(request):
		if request.method == 'POST':
			form = VideoForm(request.POST, request.FILES)
			print(request.POST.get('session_pk'))
			if form.is_valid():
				print("valid form")
				fStore = MovieHLSCreate(request.FILES['video_file_field'])
				current_ses_pk = request.POST.get('session_pk')
				current_ses = Session.objects.get(pk=current_ses_pk)
				fStore.storeMovies(current_ses)
				data ={'is_valid':True}
			else:
				data ={'is_valid':False}
			return JsonResponse(data)
	@csrf_exempt
	def csv(request):
		if request.method =='POST':
			form = CSVForm(request.POST, request.FILES)
			print(request.POST.get('session_pk'))
			if form.is_valid():
				print("valid form")
				current_ses_pk = request.POST.get('session_pk')
				current_ses = Session.objects.get(pk=current_ses_pk)
				current_ses.csv_log = request.FILES['csv_file_field']
				csvIns = CSV(current_ses)
				csvIns.createSeconds()
				data ={'is_valid':True}
			else:
				data ={'is_valid':False}
			return JsonResponse(data)











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
     session_pk = request.GET.get('session_choice')
     session = Session.objects.get(pk=session_pk)
     movies = Movie.objects.all().filter(session__pk = session_pk)

     return render(request, 'train_seg/movie_list.html', {'movie_choices':movies})


def load_tags(request):
     tag_type_recieved = request.GET.get('anal_choice')
     tags = tag.objects.filter(tag_type__pk = tag_type_recieved)

     return render(request, 'train_seg/tag_list.html', {'tag_list':tags})




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