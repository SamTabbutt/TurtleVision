from django.db import models

# Create your models here.

class Session(models.Model):
	session_id = models.CharField(max_length=20)
	turtle_id = models.IntegerField(default=0)
	record_date = models.DateField('date recorded')
	pub_date = models.DateTimeField('date published')

class Movie(models.Model):
	session = models.ForeignKey(Session, on_delete=models.CASCADE)
	video_path = models.CharField(max_length=200)
	video_title = models.CharField(max_length=20)
	video_id = models.CharField(max_length=50)