#adapted from https://realpython.com/python-csv/
import csv
import codecs
from .models import SecondDat, Session, Movie, Frame
import time
import cv2

#this CSV is expecting absolutely correct data or the whole program will crash.
#this is poor form however I will complete the original functionality then return
class CSVdump():
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
                         line_num+=1

#adapted from https://medium.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481
class FrameCreate():
     def __init__(self,sec1,src1):
          self.second=sec1
          self.source=src1
     
     def grabFrame(self):
          true_src = 'C:/Users/samta/TurtleCam/' + self.source
          vidcap = cv2.VideoCapture(true_src)
          print(true_src+"   "+str(self.second))
          vidcap.set(cv2.CAP_PROP_POS_MSEC,self.second*1000)
          hasFrames,image = vidcap.read()
          if hasFrames:
               return image