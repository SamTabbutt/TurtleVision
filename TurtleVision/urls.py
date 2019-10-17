from django.urls import path, re_path

from . import views
from TurtleVision.views import index, upload, train, trust

app_name = 'TurtleVision'
urlpatterns = [
    #index is the opening page for turtlevision
    path('', index.as_view(), name='index'),

    #upload is going to be a password protected page for admin to upload the videos and blank csv logs
    path('upload/', upload.as_view(), name='upload'),

    path('upload/success/', views.uploadSuccess, name='success'),

    #train is a view class
    #using primary key to refer to videos. may end up being a mistake. We will see
    re_path(r'^train/(?P<movie_choice>\w+)/$', train.as_view(), name='train'),

    #the saveframe function is called by ajax and implimented asynchronously
    path('ajax/saveframe/', views.saveFrame, name='saveFrame'),

    path('ajax/load-movies/', views.get_movies, name='ajax_load_movies'),

    path('ajax/load-video/', views.load_video, name='ajax_load_video'),

    #the trust view is password protected for admin to run an analysis on a session
    path('trust/', trust.as_view(), name='trust'),

]