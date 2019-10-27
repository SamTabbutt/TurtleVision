from django.db import models
from django.contrib.postgres.fields import ArrayField

# The goal of the application is to:
#	1) videos and .csv log uploaded by admin user
# 	2) database containing frames updated by common user
#	3) admin runs automatic analysis on video




# Session: when the TurtleCam is deployed, everything that happens within the timeframe between 
# when the turtle is deployed and the camera stops recording is in the context of a single session
# The session will all exist with a single turtle and recorded on a date. It is also worth
# Tracking when it was published and where the turtlecam was deployed

class Session(models.Model):
        record_date = models.DateField('date recorded', blank=True)
        loc_name = models.CharField(null=True, max_length=15)
        csv_log = models.FileField(upload_to='csv/', null=True, verbose_name="")

        def __str__(self):
                return str(self.pk)+self.loc_name+": "+str(self.record_date)


# Movie: the session contains about twenty individual movie files that comprise the entirety of
# the session. Each movie is associated with one session, but a single session may contain twenty movies
# video_path will refer to the folder containing the movie file. video_title will contain the name of the file
# video_ ID will be a unique video id containing information of the session and turtle
# video_length is important to match up data points with the row of information

class Movie(models.Model):
	session = models.ForeignKey(Session, on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	videofile=models.FileField(upload_to='videos/', null=True, verbose_name="")

	def __str__(self):
        	return str(self.pk)+": "+str(self.videofile)

class tagType(models.Model):
	name = models.CharField(max_length = 20)

	def __str__(self):
		return str(self.name)

class tag(models.Model):
        tag_type=models.ForeignKey(tagType, on_delete=models.CASCADE)
        tag_val=models.CharField(max_length=20)
        tag_num=models.IntegerField(default=0)

        def __str__(self):
             return str(self.tag_type)+":"+str(self.tag_val)

class tagAssign(models.Model):
	tag=models.ForeignKey(tag, on_delete=models.CASCADE)
	loss_at_assign=models.DecimalField(max_digits=20,decimal_places=10)
	accuracy=models.DecimalField(max_digits=20,decimal_places=10)
	assigned_by = models.CharField(max_length = 100)

	def __str__(self):
		return str(tag)+":"+str(accuracy)


# SecondDat: this datatype is considered a single "row" in the analysis of a single turtlecam video
# These instances were previously filled out manually using excel to complete the analysis
# The goal of TurtleVision is to automate this process. This datatype will be filled out
# Manually via the "Train" page of the website when an administrator is on the page
# This datatype contains the information derived from the .csv file uploaded by admin along with
# session. 

class SecondDat(models.Model):
	session = models.ForeignKey(Session, on_delete=models.CASCADE)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	depth = models.DecimalField(max_digits=3, decimal_places=1)
	temp = models.DecimalField(max_digits=3, decimal_places=1)
	seg_time = models.TimeField(blank=True, null=True)
	session_time = models.TimeField(blank=True, null=True)
	tag = models.ManyToManyField(tagAssign)

	def __str__(self):
        	return str(self.session)+":"+str(self.movie)+":"+str(self.seg_time)

# Frame: when a frame is logged to be a certain type by the user, it is added to a list of 'Frames'
# The Frame list is in development as it will be determined the exact information necesarry to log
# As the machine learning algorithm is developed.

class Frame(models.Model):
        secondCount = models.CharField(max_length=20)        
        tag = models.ForeignKey(tag, on_delete=models.CASCADE)
        imgData = models.BinaryField(blank=True)
        movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True, null=True)

        def __str__(self):
             return str(self.tag)+":"+str(self.movie)+":"+str(self.secondCount)


class learningModel(models.Model):
	tag_type = models.ForeignKey(tagType, on_delete=models.CASCADE)
	create_date_time = models.DateTimeField(auto_now=True)
	parameters_dir = models.CharField(max_length = 100)