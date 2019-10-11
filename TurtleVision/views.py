from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse


from django.urls import reverse
from django.http import HttpResponse
from django.template import loader
from .models import Session, Movie, Frame

#access the TurtleVision welcome page--index
#this is the welcome page for the Turtle Vision application. It will provide some dynamic information
#as well as a breif discription of how the project operates
def index(request):
    num_sessions = Session.objects.all().count()
    num_movies = Movie.objects.all().count()
    num_frames = Frame.objects.all().count()

    context = {
	'num_sessions':num_sessions,
	'num_movies':num_movies,
	'num_frames':num_frames,
    }

    return render(request, 'index.html', context=context)


#This is the main host page for the training option. Still working on how exactly to model the selections
#Ideally there will be dynamic choose selectors on the right panel. 
#First selection is session from session index
#second selection is movie from movie index pulled from selected session
#Third selection is type of analysis
#Based on type of analysis chosen, the panel will display different set of buttons.
def train(request):
    movieChoice = Movie.objects.get(movie_id_read="TC01MOV0001")
    context={
	'movie_choice':movieChoice
    }
    return render(request, 'train.html', context=context)

def analysisChoice(request):
    context = {

    }
    return render(request, 'sessionIndex.html', context=context)


#establishing breath button action. This function will eventually be called from a condition determined in train page
#when the breath button is pressed, the frame currently displayed will be logged as "frame" with breath boolean set to true
def breath(request, movie_id):
    try:
        selected_choice = question.choice_set.get(pk=request.POST['Frame'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))













# View accessed at initial entrance to 'train'. This is the outside list layer for sessions
# To be listed in order of session_num
# HTML referenced in index.html
# Gathers all objects under 'Session' datatype and orders them for display
def indexSession(request):
    latest_session_list = Session.objects.order_by('-session_num')
    context = {
	'latest_session_list':latest_session_list,
    }
    return render(request, 'sessionIndex.html', context=context)



# Functions in same light as indexSession. View will be accessed inside of session
def indexMovie(request, session_id_read):
    latest_movie_list = Movie.objects.filter(session__session_id_read=session_id_read).order_by('-movie_title')
    template = loader.get_template('TurtleVision/indexMovie.html')
    context = {
	'latest_movie_list':latest_movie_list,
    }
    return HttpResponse(template.render(context,request))


def movieView(request, movie_id_read):
    this_movie = get_object_or_404(Movie, movie_id_read=movie_id_read)
    return render(request, 'TurtleVision/movieView.html', {'file':this_movie})
