from numba import jit, cuda
import skvideo.io
from queue import Queue
from mxnet.gluon.data.vision import transforms as trans
from mxnet import nd
from threading import Thread
import time
import pyopencl as cl

class ndQueue():
	def __init__(self,path, movieName, queue_size=600):
		#self.stream = cv2.VideoCapture(path)
		platforms = cl.get_platforms()
		ctx = cl.Context(
			dev_type=cl.CL_DEVICE_TYPE_GPU,
			properties=[(cl.context_properties.PLATFORM, platforms[0])])
		print(cl.device_type.ALL)

		self.paramdict = skvideo.io.ffprobe(path)
		inputparameters = {}
		outputparameters = {'-r': '1', '-s':'255x255'}
		self.sk = skvideo.io.vreader(path,
                	inputdict=inputparameters,
                	outputdict=outputparameters)
		#print("Shape of input: " +str(self.sk.shape))
		self.stopped = False
		self.movie = movieName

		#self.fps = int(round(self.stream.get(cv2.CAP_PROP_FPS)))
		self.fps=30
		self.currentFrame=0
		self.Q = cl.CommandQueue(ctx)
		self.thread = Thread(target=self.update, args=())
	
	def start(self):
		print("starting queue for " +self.movie +" with fps: "+str(self.fps))
		self.thread.start()

		return self

	def update(self):
		#print(self.sk)
		for frame in self.sk:
			grabbed = True
			if self.stopped:
				break
			if not self.Q.full():
				if 0==0:
					#(grabbed,frame)=self.stream.read()
					#frame = self.sk[self.currentFrame]
					nd_non = nd.array(frame)
					print(nd_non.shape)
					transformer = trans.Compose([trans.Resize((255,255)),
						trans.CenterCrop(255),
						trans.ToTensor(),
						trans.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

					nd_img = transformer(nd_non)
					print(nd_img.shape)
					#(hasFrames,nd_img)=getNdFromFrame(grabbed,frame)
					self.Q.put(nd_img)
					print("Queued frame: "+str(self.currentFrame*30)+" for second: "+str(self.currentFrame)+" for movie: "+self.movie +"with an nd check val of: "+str(nd_img[2][54][7]))
				else:
					#self.sk.nextFrame()
					print("pointless")
					#grabbed = self.stream.grab()
				if not grabbed:
					self.stopped = True
				self.currentFrame+=1
			else:
				time.sleep(0.1)
		#self.stream.release()
	
	def read(self):
		# return next frame in the queue
		print("Queue for " +self.movie+" is stopped: " +str(self.stopped))
		return self.Q.get()

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