from django.contrib import admin

# Register your models here.

from .models import Session, Movie

admin.site.register(Session)
admin.site.register(Movie)