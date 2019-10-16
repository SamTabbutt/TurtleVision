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
    re_path(r'^train/(?P<session_choice>\w+)/(?P<movie_choice>\w+)/(?P<anal_choice>[0-9]{1})/$', train.as_view(), name='train'),

    #the saveframe function is called by ajax and implimented asynchronously
    path('train/saveframe/', views.saveFrame, name='saveFrame'),

    #the trust view is password protected for admin to run an analysis on a session
    path('trust/', trust.as_view(), name='trust'),

]