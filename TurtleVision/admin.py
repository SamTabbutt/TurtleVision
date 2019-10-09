from django.contrib import admin

# Register your models here.

from .models import Session, Movie, SecondDat

admin.site.register(Session)
admin.site.register(Movie)
admin.site.register(SecondDat)