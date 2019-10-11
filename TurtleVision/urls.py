from django.urls import path

from . import views


app_name = 'TurtleVision'
urlpatterns = [
    #train paths: these are the view formats for train
    #access session index: display all the possible session options. List display of all sessions
    path('train', views.indexSession, name='Session Index'),

    #access movies available within a session: List display of all movies within <session_num>
    path('train/<session_id_read>/', views.indexMovie, name='MovieIndex'),

    #display movie chosen from movie list with <movie_title>
    #the url will not be within a session path. From the session movie list the movie redirects
    #to a movie viewing page
    path('train/movie/<movie_id_read>/', views.movieView, name='MovieView'),
    
]