from django.contrib import admin

# Register your models here.

from .models import Session, Movie, SecondDat, Frame, tag

admin.site.register(Session)
admin.site.register(Movie)
admin.site.register(SecondDat)
admin.site.register(Frame)
admin.site.register(tag)