from django import forms

class VideoForm(forms.Form):
     session_date = forms.DateField()
     session_loc = forms.CharField(max_length=20)
     video_file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
     CSV_file_field = forms.FileField()

class VideoSelectForm(forms.Form):
     session_select = forms.CharField(max_length=100)
     movie_select = forms.CharField(max_length=100)