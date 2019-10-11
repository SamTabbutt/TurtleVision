from django.db import models

# The goal of the application is to:
#	1) videos and .csv log uploaded by admin user
# 	2) database containing frames updated by common user
#	3) admin runs automatic analysis on video




# Session: when the TurtleCam is deployed, everything that happens within the timeframe between 
# when the turtle is deployed and the camera stops recording is in the context of a single session
# The session will all exist with a single turtle and recorded on a date. It is also worth
# Tracking when it was published and where the turtlecam was deployed

class Session(models.Model):
	session_id = models.CharField(max_length=20)
	session_num = models.IntegerField(default=0)
	turtle_id = models.CharField(max_length=20)
	record_date = models.DateField('date recorded')
	pub_date = models.DateTimeField('date published')
	loc_name = models.CharField(default='CEI',max_length=15)

	def __str__(self):
        	return self.session_id



# Movie: the session contains about twenty individual movie files that comprise the entirety of
# the session. Each movie is associated with one session, but a single session may contain twenty movies
# video_path will refer to the folder containing the movie file. video_title will contain the name of the file
# video_ ID will be a unique video id containing information of the session and turtle
# video_length is important to match up data points with the row of information

class Movie(models.Model):
	session = models.ForeignKey(Session, on_delete=models.CASCADE)
	movie_path = models.CharField(max_length=200)
	movie_title = models.CharField(max_length=20)
	movie_type = models.CharField(max_length=5)
	movie_id_read = models.CharField(max_length=50)
	movie_length = models.TimeField(blank=True, null=True)

	def __str__(self):
        	return self.movie_id_read




# SecondDat: this datatype is considered a single "row" in the analysis of a single turtlecam video
# These instances were previously filled out manually using excel to complete the analysis
# The goal of TurtleVision is to automate this process. This datatype will be filled out
# Manually via the "Train" page of the website when an administrator is on the page
# This datatype contains the information derived from the .csv file uploaded by admin along with
# session. 

class SecondDat(models.Model):
	session = models.ForeignKey(Session, on_delete=models.CASCADE)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	sec_id_read = models.CharField(max_length=50)
	depth = models.DecimalField(max_digits=3, decimal_places=1)
	temp = models.DecimalField(max_digits=3, decimal_places=1)
	seg_time = models.TimeField(blank=True, null=True)
	session_time = models.TimeField(blank=True, null=True)

	def __str__(self):
        	return self.sec_id_read


# Frame: when a frame is logged to be a certain type by the user, it is added to a list of 'Frames'
# The Frame list is in development as it will be determined the exact information necesarry to log
# As the machine learning algorithm is developed.

class Frame(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	Frame_id_read = models.CharField(max_length=50)
	second_of_movie = models.TimeField(blank=True, null=True)
	breath = models.BooleanField(default=False)

	def __str__(self):
        	return self.Frame_id_read
