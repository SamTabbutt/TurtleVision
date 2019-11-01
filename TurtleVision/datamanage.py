#This file is established to make all connections between the views of the app and the models of the app



#First make all necesarry imports
#adapted from https://realpython.com/python-csv/
import csv
import sys
import time
import cv2      #need pip install
import numpy as np      #need pip install
import ffmpeg #need pip install
import pickle      #included in python 3
import base64      #included in python 3

from mxnet.gluon.data.vision import transforms as trans
from mxnet import nd
from threading import Thread
import time
from queue import Queue

from .models import SecondDat, Session, Movie, Frame, tag, learningModel
from django.conf import settings
from django.http import HttpResponse

from .dataAnalyze import applyModel

import os




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
	
	def occupySeconds(self):
		model_in_use = learningModel.objects.filter(tag_type__pk=self.anal).order_by('-create_date_time')[0]
		movie_list = Movie.objects.filter(session__pk = self.session)
		application = applyModel(self.anal,model_in_use.parameters_dir,self.session)
		start_time = time.time()
		for movie in movie_list:
			second_list = SecondDat.objects.filter(movie__pk = movie.pk)
			for second in second_list:
				sec = second.seg_time
				src = '/media/'+str(second.movie.videofile)
				tag = 0
				(h, m, s) = str(sec).split(':')
				result = int(h) * 3600 + int(m) * 60 + int(s)
				print(src)
				newFrame = FrameCreate(result, src, tag)
				(hasFrames,image) = newFrame.getFrameFromSec()
				(hasFrames,nd_img) = getNdFromFrame(hasFrames,image)
				print(hasFrames)
				if(hasFrames):
					application.saveSecond(nd_img, sec, second)
		elapsed_time = time.time() - start_time
		print(elapsed_time)
				

class FileVideoStream():
	def __init__(self, path, transform=None, queue_size=128):
		# initialize the file video stream along with the boolean
		# used to indicate if the thread should be stopped or not
		self.stream = cv2.VideoCapture(path)
		self.stopped = False
		self.transform = transform

		self.fps = int(round(self.stream.get(cv2.CAP_PROP_FPS)))
		self.currentFrame=0

		# initialize the queue used to store frames read from
		# the video file
		self.Q = Queue(maxsize=queue_size)
		# intialize thread
		self.thread = Thread(target=self.update, args=())
		self.thread.daemon = True

	def start(self):
		print("current frame:" +str(self.currentFrame))
		print("fps:"+str(self.fps))

		# start a thread to read frames from the file video stream
		self.thread.start()
		return self

	def update(self):
		# keep looping infinitely
		while True:
			# if the thread indicator variable is set, stop the
			# thread
			if self.stopped:
				break

			# otherwise, ensure the queue has room in it
			if not self.Q.full():
				# read the next frame from the file

				(grabbed, frame) = self.stream.read()

				if not grabbed:
					self.stopped = True
					
				if self.transform:
					frame = self.transform(frame)

				if self.currentFrame%self.fps==0:
					self.Q.put(frame)
					print("Logged: "+str(self.currentFrame)+"frameid: " +str(frame[25][42]))
				self.currentFrame+=1

			else:
				time.sleep(0.1)  # Rest for 10ms, we have a full queue

		self.stream.release()

	def read(self):
		# return next frame in the queue
		print(self.stopped)
		return self.stopped, self.Q.get()

	# Insufficient to have consumer use while(more()) which does
	# not take into account if the producer has reached end of
	# file stream.
	def running(self):
		return self.more() or not self.stopped

	def more(self):
		# return True if there are still frames in the queue. If stream is not stopped, try to wait a moment
		tries = 0
		while self.Q.qsize() == 0 and not self.stopped and tries < 5:
			time.sleep(0.1)
			tries += 1

		return self.Q.qsize() > 0

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
		# wait until stream resources are released (producer thread might be still grabbing frame)
		self.thread.join()


				


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
