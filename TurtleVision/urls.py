from django.urls import path

from . import views

app_name = 'TurtleVision'
urlpatterns = [
    #index is the opening page for turtlevision
    path('', views.index, name='index'),

    #train is the guest user's first option
    path('train/', views.train, name='train'),

    path('analysis/', views.analysisChoice, name='analysisChoice'),


    #train paths: these are the view formats for train
    #access session index: display all the possible session options. List display of all sessions
    path('session/', views.indexSession, name='sessionIndex'),

    #access movies available within a session: List display of all movies within <session_num>
    path('<session_id_read>/', views.indexMovie, name='MovieIndex'),

    #display movie chosen from movie list with <movie_title>
    #the url will not be within a session path. From the session movie list the movie redirects
    #to a movie viewing page
    path('movie/<movie_id_read>/', views.movieView, name='MovieView'),

]