from django.urls import path, re_path

from . import views
from TurtleVision.views import index, upload, train, trust

app_name = 'TurtleVision'
urlpatterns = [
    #URL for welcome page
    #returns rendered 'index.html'
    path('', index.as_view(), name='index'),

    #upload is going to be a password protected page for admin to upload the videos and blank csv logs
    path('upload/', upload.as_view(), name='upload'),

    path('upload/success/', views.uploadSuccess, name='success'),

    #train is a view class
    path('train/', train.as_view(), name='train'),

    #the saveframe function is called by ajax and implimented asynchronously
    path('ajax/saveframe/', views.saveFrame, name='saveFrame'),

    path('ajax/load-movies/', views.get_movies, name='ajax_load_movies'),

    path('ajax/load-video/', views.load_video, name='ajax_load_video'),

    #the trust view is password protected for admin to run an analysis on a session
    path('trust/', trust.as_view(), name='trust'),

    path('export/CSV_from_session/<session_id>', views.returnCSV, name='return_csv'),

    path('dataAnalyze/upload_and_train/<an_type>', views.loadAndTrain, name='load_and_train'),

    path('dataAnalyze/update_seconds/<session_id>/<an_type>',views.occupySecondDat, name='occupy_seconds'),

]