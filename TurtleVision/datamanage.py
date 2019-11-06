#This file is established to make all connections between the views of the app and the models of the app



#First make all necesarry imports
#adapted from https://realpython.com/python-csv/
import csv
import sys
import time
#import cv2      #need pip install
import numpy as np      #need pip install
import ffmpeg #need pip install
import pickle      #included in python 3
import base64      #included in python 3

from mxnet.gluon.data.vision import transforms as trans
from mxnet import nd
from threading import Thread
from multiprocessing import Process
import time
from queue import Queue

import skvideo.io
import skvideo.datasets

skvideo.setFFmpegPath('ffmpeg-4.0.2-win64-static/bin/')

import pyopencl as cl

import ffmpeg

from numba import cuda, jit
import numba

import django
django.setup()
from .models import SecondDat, Session, Movie, Frame, tag, learningModel
from .GPUQueue import ndQueue
from django.conf import settings
from django.http import HttpResponse

from .dataAnalyze import applyModel

import os
import gc




#The CSV class takes input of an established session
#Each established session accompanies the log data in a csv file
#Each row of the log data represents a second of the session
#CSV is meant to parse through the csv file and create an instance of SecondDat for each row recorded
#This will be used at a later time for exporting for use by marine ecologists

#this CSV is currently expecting absolutely correct data or the whole program will crash.
#this is poor form however I will complete the original functionality then return
class CSV():
	def __init__(self, sessionI):
		self.session = sessionI

	def createSeconds(self):
		with open(self.session.csv_log.path, 'r') as f:
			reader = csv.reader(f, delimiter=',')
			line_num=1
			last_vid_name = "old"
			segTime = 1
			actual_time = 1
			for row in reader:
				if line_num==1:
					line_num+=1
				else:
					temp1 = float(row[1])
					depth1 = float(row[2])
					vid_name = row[3]
					session_id = self.session.pk
					if last_vid_name!=vid_name:
						segTime=1
						last_vid_name=vid_name
					else:
						segTime+=1
					newSec = SecondDat(session=Session.objects.get(pk=session_id), movie = Movie.objects.all().filter(session__pk=session_id).all().filter(name__contains=vid_name).get(), depth=depth1, temp=temp1, seg_time=time.strftime('%H:%M:%S', time.gmtime(segTime)), session_time=time.strftime('%H:%M:%S', time.gmtime(actual_time)))
					newSec.save()
					actual_time+=1
					line_num+=1

	def secondsToCSV(self):
		current_ses = self.session
		response = HttpResponse(content_type='text/csv')
		response ['Content-Disposition'] = 'attachment; filename="csv_database_write.csv"'
	
		writer = csv.writer(response)
		firstrowList = ['Session Time','Segment Time','Movie','Session Number','Date','Location','Depth','Temperature']
		alltags = tag.objects.all().values('tag_type').distinct()
		for tagtype in alltags:
			firstrowList.append(str(tagtype))
			firstrowList.append('Confidence')
			firstrowList.append('Tagged By')
		writer.writerow(firstrowList)

		for second in current_ses:
			currentSecList = [second.session_time, second.seg_time, second.movie.name, second.session.pk, str(second.session.record_date),second.session.loc_name, second.depth,second.temp]
			for t in second.tag.all():
				currentSecList.append(t.tag.tag_val)
				currentSecList.append(str(t.accuracy))
				currentSecList.append(str(t.assigned_by))
			writer.writerow(currentSecList)
		return response


#FrameCreate class takes a second value and a source value and returns a binary-encoded numpy file
#The binary-encoded numpy file is saved with an associated tag which labels what the frame was saved as


def getNdFromFrame(hasFrames, image):
     if hasFrames:
          #reorganize later.. make class in dataAnalyze
          img_nump = np.asarray(image)
          temp_nd = nd.array(img_nump)


          transformer = trans.Compose([trans.Resize(300),
                                           trans.CenterCrop(255),
                                           trans.ToTensor(),
                                           trans.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

          norm_nd_img = transformer(temp_nd)
          return hasFrames,norm_nd_img
     else:
          return hasFrames,'null'

#numpy pickle stuff https://stackoverflow.com/questions/46699238/how-to-make-a-numpy-array-field-in-django
#adapted from https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481
class FrameCreate():
     def __init__(self,sec1,src1,tag1):
          self.second=sec1
          self.source=src1
          self.tag=tag1

     def createFrameInstance(self):
          get_src = str(self.source)[7:]
          src_movie = Movie.objects.all().get(videofile=get_src)
          (hasFrames, image) = self.getFrameFromSec()
          (hasFrames, norm_nd) = getNdFromFrame(hasFrames, image)
          if hasFrames:
               get_im = self.grabNdBinary(norm_nd)
               new_tag = self.getTag()

               new_frame = Frame(tag=new_tag, secondCount=self.second, imgData = get_im, movie=src_movie)
               new_frame.save()
               print("Logged " +new_tag.tag_val+ " tag from " +str(self.second) +" second")
          else:
               print("Frame not found. Not logged")


     def getFrameFromSec(self):
          #use cv2 to capture a frame at self.second from self.source to return imagedata [H x W x RGB]
          RootSrc = "C:/Users/samta/TurtleCam"+self.source
          vidcap = cv2.VideoCapture(RootSrc)


          #perhaps a much quicker method for grabbing frames https://gist.github.com/kylemcdonald/85d70bf53e207bab3775
          #This function takes an incredibly long time to execute
          vidcap.set(cv2.CAP_PROP_POS_MSEC,self.second*1000)

          (hasFrames,image) = vidcap.read() #stored as 3-D list [H][W][RGB]

          return (hasFrames,image)


     def grabNdBinary(self, norm_nd_img):
          
          norm_nump = norm_nd_img.asnumpy()
          
          np_bytes = pickle.dumps(norm_nump)
          np_base64 = base64.b64encode(np_bytes)

          return np_base64

     def getTag(self):
          return tag.objects.get(tag_num=self.tag)

#used https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/ to achieve fast loading
class fillSession():
	def __init__(self,session, anal):
		self.session = session
		self.anal = anal
		self.model_in_use = learningModel.objects.filter(tag_type__pk=self.anal).order_by('-create_date_time')[0]
		self.application = applyModel(self.anal,self.model_in_use.parameters_dir,self.session)

	def occupySeconds(self):
		movie_list = Movie.objects.filter(session__pk = self.session)
		start_time = time.time()
		jobs = []
		platforms = cl.get_platforms()
		print(len(platforms))
		print(platforms)
		print(platforms[1].get_devices(cl.device_type.GPU))
		ctx = cl.Context(
			dev_type=cl.device_type.GPU,
			properties=[(cl.context_properties.PLATFORM, platforms[0])])

		with cl.CommandQueue(self.cl_context) as queue:
			for movie in movie_list:
				self.fillMovie(movie)

	def fillMovie(self,movie):
		print("starting process for movie:"+str(movie))	
			
		src = '/media/'+str(movie.videofile)
		RootSrc = "C:/Users/samta/TurtleCam"+src
		queue = ndQueue(RootSrc,str(movie)).start()
		second_list = SecondDat.objects.filter(movie__pk = movie.pk).order_by('seg_time')
		time.sleep(10)				
		for second in second_list:
			if queue.running():
				sec = second.seg_time
				nd_img = queue.read()
				print(str(movie)+": "+str(sec)+": analyzing with nd frame check: "+str(nd_img[2][54][7]))
				self.application.saveSecond(nd_img, sec, second)
			else:
				queue.stop()
				break
		gc.collect()
			

	
				

#TO-DO: finish for deployment (for first deploy). At the moment in its first stage
#adapting movie upload so the movies can be in HLS format.
#going to display it on frontend using https://github.com/videojs/http-streaming#documentation
#storing it on backend using https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming
#using async upload: https://simpleisbetterthancomplex.com/tutorial/2016/11/22/django-multiple-file-upload-using-ajax.html


class MovieHLSCreate():
     def __init__(self, t):
          self.Movie=t
     
     def storeMovies(self, current_ses):
          print("here")
          n = str(self.Movie)
          #transfer f to HLS format for storage
          #fHLS = HLSForm(f)
          #print("made it")
          #handle_uploaded_file(f)
          newM = Movie(session = current_ses, name = n, videofile = self.Movie)
          newM.save()

def handle_uploaded_file(f):
	print(f.multiple_chunks())
	return

#adopted from https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/blob/master/examples/hls/hls.py

def HLSForm(f):
    input_stream = ffmpeg.input(f.temporary_file_path(), f='mp4')
    output_stream = ffmpeg.output(input_stream, f.temporary_file_path(), format='hls', start_number=0, hls_time=5, hls_list_size=0)
    return output_stream
