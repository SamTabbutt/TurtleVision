from django import forms

class SessionForm(forms.Form):
     session_date = forms.DateField()
     session_loc = forms.CharField(max_length=20)
     session_turtle = forms.CharField(max_length=20)

class VideoForm(forms.Form):
	session_pk = forms.CharField()
	video_file_field = forms.FileField()

class CSVForm(forms.Form):
	session_pk = forms.CharField()
	csv_file_field = forms.FileField()