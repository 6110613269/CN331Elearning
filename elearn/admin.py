from django.contrib import admin
from .models import *
from django.apps import apps
# Register your models here.

class CourseList(admin.ModelAdmin):
    list_display = ("subjectid", "subject", "subscribe")
    
    
class VideoList(admin.ModelAdmin):
    list_display = ("subjectid", "videoname")
    

class FileList(admin.ModelAdmin):
    list_display = ("subjectid", "filename")
    
admin.site.register(SubjectSubscribe, CourseList)
admin.site.register(Video, VideoList)
admin.site.register(File, FileList)