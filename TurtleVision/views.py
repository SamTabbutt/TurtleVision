from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.urls import reverse
from django.http import HttpResponse
from django.template import loader
from .models import Session, Movie



# View accessed at initial entrance to 'train'. This is the outside list layer for sessions
# To be listed in order of session_num
# HTML referenced in index.html
# Gathers all objects under 'Session' datatype and orders them for display
def indexSession(request):
    latest_session_list = Session.objects.order_by('-session_num')
    template = loader.get_template('TurtleVision/index.html')
    context = {
	'latest_session_list':latest_session_list,
    }
    return HttpResponse(template.render(context,request))



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

def markBreath