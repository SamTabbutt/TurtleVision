from django.contrib import admin

# Register your models here.

from .models import Session, Movie, SecondDat, Frame, tag, tagType, learningModel, tagAssign
admin.site.register(Session)
admin.site.register(Movie)
admin.site.register(SecondDat)
admin.site.register(Frame)
admin.site.register(tag)
admin.site.register(tagType)
admin.site.register(learningModel)
admin.site.register(tagAssign)